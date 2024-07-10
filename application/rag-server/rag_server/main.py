import logging
from datetime import datetime

import uvicorn
from api_types import ChatHistoryResponse, ChatRequest, PromptFnCalls
from data_utils import init_data_utils
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
        fn_resp = {
            "user_prompt": request.prompt,
            "fn_calls": fn_calls
        }
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


def init_server():
    logger.info("Running server initialization ...")
    init_data_utils()
    init_llm_handler()
    logger.info("Server is ready to handle requests")


# Allow running of app from direct python invocation
if __name__ == "__main__":
    init_server()
    uvicorn.run(app, host="0.0.0.0", port=8000)
