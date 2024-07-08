from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException
from llm.llm_handler import run_chat_loop
from pydantic import BaseModel


class PromptRequest(BaseModel):
    prompt: str


app = FastAPI()


@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/api/v1/chat")
async def generate_message(request: PromptRequest):
    try:
        # TODO add prompt validation
        output_msgs = run_chat_loop(request.prompt)
        output_str = "\n".join(output_msgs)
        return {"message": output_str}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Allow running of app from direct python invocation
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
