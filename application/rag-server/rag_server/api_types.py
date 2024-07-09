from typing import List, Union

from fastapi import FastAPI
from pydantic import BaseModel, validator

app = FastAPI()


class ToolUseInput(BaseModel):
    queries: List[str]


class ToolUseContent(BaseModel):
    type: str
    id: str
    name: str
    input: ToolUseInput  # TODO: replace with a union of function args


class ToolResultContent(BaseModel):
    type: str
    tool_use_id: str
    content: str


class TextContent(BaseModel):
    type: str
    text: str


class Message(BaseModel):
    role: str
    content: List[Union[TextContent, ToolUseContent, ToolResultContent]]

    @validator("role")
    def validate_role(cls, value):
        if value not in {"system", "user", "assistant"}:
            raise ValueError("Role must be either 'system', 'user' or 'assistant'")
        return value


class ChatRequest(BaseModel):
    # Any existing state from previous dialogue, or an empty list if this is the first prompt
    existing_chat_history: List[Message]

    # This is always a user prompt to start or continue existing dialogue
    # tool messages are handled on the server independent of the client
    prompt: str


class ChatHistoryResponse(BaseModel):
    # The raw text response generated by the LLM for the current prompt request
    llm_response_text: str

    # The existing chat history, with the newly added messages
    # this includes any tool calls, tool responses, and the llm response
    new_chat_history: List[Message]