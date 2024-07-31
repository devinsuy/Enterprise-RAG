from enum import Enum
from typing import Any, Dict, List, Optional, Union

from fastapi import FastAPI
from pydantic import BaseModel, Field, validator

from llm.prompts import baseline_sys_prompt

app = FastAPI()


def default_config_params():
    return ConfigParams()


class ToolUseInput(BaseModel):
    queries: List[str]

    class Config:
        extra = "forbid"


class ToolUseContent(BaseModel):
    type: str
    id: str
    name: str
    input: Any

    class Config:
        extra = "forbid"


class ToolResultContent(BaseModel):
    type: str
    tool_use_id: str
    content: str

    class Config:
        extra = "forbid"


class TextContent(BaseModel):
    type: str
    text: str

    class Config:
        extra = "forbid"


class Message(BaseModel):
    role: str
    content: List[Union[TextContent, ToolUseContent, ToolResultContent]]

    @validator("role")
    def validate_role(cls, value):
        if value not in {"system", "user", "assistant"}:
            raise ValueError("Role must be either 'system', 'user' or 'assistant'")
        return value

    class Config:
        extra = "forbid"


class DocRetreiver(str, Enum):
    coarse = "coarse"
    reranker = "reranker"
    self_query_chain = "self_query_chain"


class CoarseSearchType(str, Enum):
    similarity = "similarity"
    mmr = "mmr"


class SelfQueryApi(str, Enum):
    OpenAI = "OpenAI"
    Azure = "Azure"


# Allows options to override system config, uses default values if omitted
class ConfigParams(BaseModel):
    # Bedrock parameters
    top_p: Optional[float] = 0.9
    top_k: Optional[int] = 2
    temperature: Optional[float] = 0.5
    max_tokens: Optional[int] = 3000
    system_prompt: Optional[str] = baseline_sys_prompt

    # Retriever parameters
    retriever: Optional[DocRetreiver] = DocRetreiver.coarse

    coarse_search_type: Optional[CoarseSearchType] = CoarseSearchType.similarity
    coarse_top_k: Optional[int] = 5
    coarse_lambda: Optional[float] = 0.5

    reranker_top_n: Optional[int] = 1
    coarse_fetch_k: Optional[int] = 100  # mmr only

    self_query_api: Optional[SelfQueryApi] = SelfQueryApi.OpenAI
    self_query_model: Optional[str] = "gpt-4o-mini"

    class Config:
        extra = "forbid"


class DynamicTunersRequest(BaseModel):
    # Any existing state from previous dialogue, or an empty list if this is the first prompt
    existing_chat_history: List[Message]

    # Tuners generated from the previous iteration, if any
    previous_tuners: Optional[List[str]] = []

    # Config overrides, NOTE: only generation configs are used since retrival is not relevant
    config: ConfigParams = Field(default_factory=default_config_params)

    class Config:
        extra = "forbid"


class ChatRequest(BaseModel):
    # Any existing state from previous dialogue, or an empty list if this is the first prompt
    existing_chat_history: List[Message]
    # This is always a user prompt to start or continue existing dialogue
    prompt: str
    config: ConfigParams = Field(default_factory=default_config_params)

    class Config:
        extra = "forbid"


class PromptFnCalls(BaseModel):
    # The initial prompt the user sent to the server
    user_prompt: str

    # The list of function calls the model made
    fn_calls: List[Union[ToolResultContent, TextContent]]

    class Config:
        extra = "forbid"


class ChatHistoryResponse(BaseModel):
    # The raw text respons4e generated by the LLM for the current prompt request
    llm_response_text: str

    # The existing chat history, with the newly added messages
    # this includes any tool calls, tool responses, and the llm response
    new_chat_history: List[Message]

    # fn_calls: PromptFnCalls
    fn_calls: Any  # FIX THIS

    class Config:
        extra = "forbid"


class DocsQueryRequest(BaseModel):
    queries: List[str]

    class Config:
        extra = "forbid"


class DocumentResponse(BaseModel):
    page_content: str
    metadata: dict

    class Config:
        extra = "forbid"


class DocsQueryResponse(BaseModel):
    queries: Dict[str, List[DocumentResponse]]

    class Config:
        extra = "forbid"


class TestQueriesRequest(BaseModel):
    test_queries: Optional[List[str]] = None
    use_gatekeeper_queries: Optional[bool] = False
    config: ConfigParams = Field(default_factory=ConfigParams)
    existing_state: Optional[Dict[str, Any]] = None

    class Config:
        extra = "forbid"
