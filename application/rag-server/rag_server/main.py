import asyncio
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import boto3
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from pydantic import ValidationError
from test_queries import gate_keeper_queries, test_queries

from api_types import (ChatHistoryResponse, ChatRequest, CoarseSearchType,
                       DocRetreiver, DocsQueryRequest, DocsQueryResponse,
                       DocumentResponse, TestQueriesRequest)
from constants import BUCKET_NAME_TESTING
from data_utils import handle_vector_db_queries, initialize_vector_db
from llm.llm_handler import run_chat_loop
from retrieval_utils import initialize_retrieval_chain, intialize_reranker

# Load env vars
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

logger.info("Initialize s3 client")
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)

# DB & retriever init, reuse singleton instances
logger.info("Initializing document db retrievers")

# Pre-requisite: allow initialize_qdrant.py to complete before running this file
# We configure this way so concurrent workers don't re-initialize the db each time
store = initialize_vector_db(needs_init=False)

app = FastAPI()

# Allow local development and deployed client app to make CORS requests
origins = [
    "http://localhost:3000",
    "https://main.d3juqriobddbo7.amplifyapp.com",
    "https://scraps2scrumptious.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# API key dependency
API_KEY_NAME = "Authorization"
API_KEY = os.getenv("API_KEY")

# We would never do this in a real server, but it's convenient in debugging for now
logger.info(f"Server is configured to expect api key: {API_KEY}")

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


# Dynamically determine doc retriever based on request
# defaults to coarse if no retriever was specified
def get_retriever(config):
    # Initialize coarse retriever regardless as its used for all types
    if config.coarse_search_type == CoarseSearchType.similarity:
        coarse_retriever = store.as_retriever(
            search_type=CoarseSearchType.similarity,
            search_kwargs={"k": config.coarse_top_k},
        )
    else:
        coarse_retriever = store.as_retriever(
            search_type=CoarseSearchType.mmr,
            search_kwargs={
                "k": config.coarse_top_k,
                "lambda_mult": config.coarse_lambda,
                "fetch_k": config.coarse_fetch_k,
            },
        )

    if config.retriever == DocRetreiver.reranker:
        return intialize_reranker(coarse_retriever, config)
    elif config.retriever == DocRetreiver.self_query_chain:
        return initialize_retrieval_chain(coarse_retriever, config)
    else:
        return coarse_retriever


async def get_api_key(request: Request, api_key_header: str = Depends(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        headers = {k: v for k, v in request.headers.items()}
        logger.warning(
            f"Invalid API key: {api_key_header}. Received headers: {headers}"
        )
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials, was the correct value passed for the {API_KEY_NAME} header? Received headers: {headers}",
        )


@app.get("/v1/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/v1/chat")
async def generate_message(request: ChatRequest, api_key: str = Depends(get_api_key)):
    print(f"Running /chat request with config {request.config}")
    doc_retriever = get_retriever(request.config)
    try:
        chat_history_as_dicts = [
            message.model_dump() for message in request.existing_chat_history
        ]
        model_text_output, updated_chat_history, fn_calls = run_chat_loop(
            chat_history_as_dicts, request.prompt, doc_retriever, request.config
        )
        fn_resp = {"user_prompt": request.prompt, "fn_calls": fn_calls}
        return ChatHistoryResponse(
            llm_response_text=model_text_output,
            new_chat_history=updated_chat_history,
            fn_calls=fn_resp,
        )
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except ValueError as e:
        logger.error(f"Value error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/v1/recipes/query", response_model=DocsQueryResponse)
async def query_documents(
    request: DocsQueryRequest, api_key: str = Depends(get_api_key)
):
    print(f"Running /recipes/query request with config {request.config}")
    doc_retriever = get_retriever(request.config)
    try:
        document_objects = handle_vector_db_queries(request.queries, doc_retriever)
        serialized_docs = [
            DocumentResponse(page_content=doc.page_content, metadata=doc.metadata)
            for doc in document_objects
        ]
        return DocsQueryResponse(documents=serialized_docs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def process_query(i, query, config):
    entry = {
        "Query_Question_No": i,
        "Query_Question": query,
        "Config_Params": config.model_dump(),  # Include the full config used for generation
    }
    try:
        chat_request = ChatRequest(
            existing_chat_history=[], prompt=query, config=config
        )
        response = await generate_message(chat_request)
        entry["Query_Response"] = response.llm_response_text
    except Exception as e:
        err = f"Error occurred during generation: {e}"
        entry["Query_Response"] = err
    return i, entry


@app.post("/v1/recipes/test_queries")
async def run_test_prompts(
    request: TestQueriesRequest, api_key: str = Depends(get_api_key)
):
    print(f"Running /recipes/test_queries request with config {request.config}")
    queries = request.test_queries if request.test_queries else test_queries

    to_save = {}
    tasks = [
        process_query(i, query, request.config)
        for i, query in enumerate(queries, start=1)
    ]
    results = await asyncio.gather(*tasks)

    for i, result in results:
        to_save[f"Entry_{i}"] = result

    if request.file_name:
        results_file_name = request.file_name
    else:
        current_time = datetime.now().strftime("%m-%d-%H-%M")
        config_part = (
            f"_{request.config.retriever}_top_p_{request.config.top_p}_top_k_{request.config.top_k}_temp_{request.config.temperature}"
            if request.config
            else "default_config"
        )
        results_file_name = f"test_queries_results{config_part}_{current_time}.json"

    try:
        file_content = json.dumps(to_save)
        s3_client.put_object(
            Bucket=BUCKET_NAME_TESTING, Key=results_file_name, Body=file_content
        )
        return to_save
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving to S3: {e}")
