import logging
import os
from datetime import datetime

import uvicorn
from api_types import (ChatHistoryResponse, ChatRequest, DocsQueryRequest,
                       DocsQueryResponse, DocumentResponse, PromptFnCalls,
                       TestQueriesRequest)
from data_utils import handle_vector_db_queries, init_data_utils
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from llm.llm_handler import init_llm_handler, run_chat_loop
from pydantic import ValidationError

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

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
# Set an entry in .env for this value
# All requests the api must pass the key as header
API_KEY_NAME = "API_KEY"
API_KEY = os.getenv(API_KEY_NAME)

# We would never do this in a real server, but it's convenient in debugging for now
logger.info(f"Server is configured to expect api key: {API_KEY}")

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


async def get_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials, was the correct value passed for the {API_KEY_NAME} header?",
        )


@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/api/v1/chat")
async def generate_message(request: ChatRequest, api_key: str = Depends(get_api_key)):
    try:
        chat_history_as_dicts = [
            message.model_dump() for message in request.existing_chat_history
        ]
        model_text_output, updated_chat_history, fn_calls = run_chat_loop(
            chat_history_as_dicts, request.prompt
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


@app.post("/api/v1/recipes/query", response_model=DocsQueryResponse)
async def query_documents(
    request: DocsQueryRequest, api_key: str = Depends(get_api_key)
):
    try:
        document_objects = handle_vector_db_queries(request.queries, document_retriever)
        serialized_docs = [
            DocumentResponse(page_content=doc.page_content, metadata=doc.metadata)
            for doc in document_objects
        ]
        return DocsQueryResponse(documents=serialized_docs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/recipes/test_queries")
async def run_test_prompts(file_name: str, api_key: str = Depends(get_api_key)):
    import json

    import boto3
    from constants import BUCKET_NAME_TESTING, config_test_dict

    f = open("../tests/test_queries.json")
    test_set = json.load(f)
    if len(test_set) == 0:
        raise HTTPException(
            status_code=500,
            detail="No test queries provided. Check 'test_queries.json' in test folder",
        )
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    to_save = {}
    for key, query in test_set.items():
        to_save[f"Entry_{key}"] = {"Query_Question_No": key, "Query_Question": query}

        try:
            request = ChatRequest(existing_chat_history=[], prompt=query)
            response = await generate_message(request)
            to_save[f"Entry_{key}"]["Query_Response"] = response.llm_response_text

        except Exception as e:
            err = f"Error occurred during generation: {e}"
            to_save[f"Entry_{key}"]["Query_Response"] = err

        for config_name, var in config_test_dict.items():
            to_save[f"Entry_{key}"][config_name] = var

    try:
        file_content = json.dumps(to_save)
        s3_client.put_object(
            Bucket=BUCKET_NAME_TESTING, Key=file_name, Body=file_content
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving to S3: {e}")


def init_server():
    logger.info("Running server initialization ...")
    init_data_utils()
    init_llm_handler()
    logger.info("Server is ready to handle requests")


if __name__ == "__main__":
    init_server()
    from llm.llm_handler import document_retriever

    uvicorn.run(app, host="0.0.0.0", port=8000)
