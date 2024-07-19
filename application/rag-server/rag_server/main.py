import logging
import os
from datetime import datetime

import uvicorn
from api_types import (ChatHistoryResponse, ChatRequest, DocsQueryRequest,
                       DocsQueryResponse, DocumentResponse, PromptFnCalls,
                       TestQueriesRequest)
from data_utils import handle_vector_db_queries, init_data_utils
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from llm.llm_handler import init_llm_handler, run_chat_loop
from pydantic import ValidationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Allow local development of client to make CORS requests
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/api/v1/chat")
async def generate_message(request: ChatRequest):
    try:
        # Bedrock expects a json serializable list of dicts
        # serialize each pydantic message model first
        chat_history_as_dicts = [
            message.model_dump() for message in request.existing_chat_history
        ]
        model_text_output, updated_chat_history, fn_calls = run_chat_loop(
            chat_history_as_dicts, request.prompt
        )
        # print("TRYING TO CREATE WITH")
        # print(fn_calls)
        # fn_resp = PromptFnCalls(user_prompt=request.prompt, fn_calls=fn_calls)

        # FIX THIS
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
async def query_documents(request: DocsQueryRequest):
    try:
        document_objects = handle_vector_db_queries(request.queries, document_retriever)

        # Serialize the document objects
        serialized_docs = [
            DocumentResponse(page_content=doc.page_content, metadata=doc.metadata)
            for doc in document_objects
        ]

        return DocsQueryResponse(documents=serialized_docs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/api/v1/recipes/test_queries")
async def run_test_prompts(file_name: str):
    from llm.prompts import test_query_dict
    from constants import config_test_dict, BUCKET_NAME_TESTING
    import boto3
    import json

    try:
        s3_client = boto3.client('s3',
                                 aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                                 aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

        if len(test_query_dict) == 0:
            raise HTTPException(status_code=500, detail="No test queries provided. Check 'prompts.py'")

        to_save = {}
        for key, query in test_query_dict.items():

            to_save[key] = {"query": query, "response": "", "config": {}}

            request = ChatRequest(existing_chat_history=[], prompt=query)
            response = await generate_message(request)
            to_save[key]['response'] = response.llm_response_text

    except Exception as e:
        to_save[key]['response'] = f"Error occurred during generation: {e}"

    to_save[key]['config'] = config_test_dict

    try:
        file_content = json.dumps(to_save)
        s3_client.put_object(Bucket=BUCKET_NAME_TESTING, Key=file_name,
                             Body=file_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving to S3: {e}")

def init_server():
    logger.info("Running server initialization ...")
    init_data_utils()
    init_llm_handler()
    logger.info("Server is ready to handle requests")


# Allow running of app from direct python invocation
if __name__ == "__main__":
    init_server()
    from llm.llm_handler import \
        document_retriever  # Only import retriever after it's defined

    uvicorn.run(app, host="0.0.0.0", port=8000)
