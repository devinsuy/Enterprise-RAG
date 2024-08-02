export interface ToolUseInput {
  queries: string[]
}

export interface ToolUseContent {
  type: string
  id: string
  name: string
  input: ToolUseInput // TODO: replace with a union of function args
}

export interface ToolResultContent {
  type: string
  tool_use_id: string
  content: string
}

export interface TextContent {
  type: string
  text: string
}

export type MessageContent = TextContent | ToolUseContent | ToolResultContent

export interface LLMMessage {
  role: string
  content: MessageContent[]
}

export interface PromptFnCalls {
  user_prompt: string
  fn_calls: MessageContent[]
}

export interface ChatHistoryResponse {
  // The raw text response generated by the LLM for the current prompt request
  llm_response_text: string

  // The existing chat history, with the newly added messages
  // this includes any tool calls, tool responses, and the llm response
  new_chat_history: LLMMessage[]

  fn_calls: PromptFnCalls
}

export interface ChatMessage {
  id: string
  user: string
  text: string
  timestamp: string
}
