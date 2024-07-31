import json
import logging

import boto3
from botocore.config import Config
from dotenv import load_dotenv

from constants import MODEL_ID
from data_utils import format_docs, get_secret, handle_vector_db_queries
from google_search import handle_google_web_search

from .message_utils import generate_message, generate_tool_message
from .tools import google_web_search_tool, recipe_db_query_tool

# Ensure AWS creds always load before bedrock client is instantiated
load_dotenv()

logger = logging.getLogger(__name__)

boto_config = Config(
    read_timeout=100000,
)
bedrock_client = boto3.client(
    "bedrock-runtime",
    config=boto_config,
    region_name="us-east-1",
)
google_search_api_key = get_secret("google_search_api_key")


def query_bedrock_llm(messages, config):
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": messages,
        "tools": [recipe_db_query_tool, google_web_search_tool],
        "system": str(config.system_prompt),
        "max_tokens": int(config.max_tokens),
        "temperature": float(config.temperature),
        "top_p": float(config.top_p),
        "top_k": int(config.top_k),
    }
    response = bedrock_client.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(payload),
    )
    response_body = json.loads(response.get("body").read())
    return response_body


def query_bedrock_llm_streaming(messages, config):
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": messages,
        "tools": [recipe_db_query_tool, google_web_search_tool],
        "system": str(config.system_prompt),
        "max_tokens": int(config.max_tokens),
        "temperature": float(config.temperature),
        "top_p": float(config.top_p),
        "top_k": int(config.top_k),
    }
    logger.info("Query payload: %s", payload)
    response = bedrock_client.invoke_model_with_response_stream(
        modelId=MODEL_ID,
        body=json.dumps(payload),
    )
    logger.info("Received response from Bedrock")
    logger.info(response['body'])
    return response["body"]

"""
Example response body structure:
{
   "id":"msg_bdrk_01C5GGkafK7aL3P5i3rsMr1p",
   "type":"message",
   "role":"assistant",
   "model":"claude-3-sonnet-20240229",
   "content":[
      {
         "type":"tool_use",
         "id":"toolu_bdrk_01CQiYa8BMJfpJC68DuRdwQn",
         "name":"query_food_recipe_vector_db",
         "input":{
            "queries":[
               "healthy fish dinner recipe under 500 calories",
               "fish dinner recipe for two under 40 minutes"
            ]
         }
      }
   ],
   "stop_reason":"tool_use",
   "stop_sequence":"None",
   "usage":{
      "input_tokens":559,
      "output_tokens":55
   }
}
"""


def message_handler(existing_chat_history, prompt, config, is_tool_message=False):
    # Fn results is an array of tool response objects
    # message structure needs to reflect that
    if is_tool_message:
        user_message = generate_tool_message(prompt)
    else:
        user_message = generate_message(prompt)
    existing_chat_history.append(user_message)

    # Parse the response content
    response_body = query_bedrock_llm(existing_chat_history, config)
    llm_message = {"role": response_body["role"], "content": response_body["content"]}

    # Add the response message to the chat history
    existing_chat_history.append(llm_message)

    return [response_body, llm_message, existing_chat_history]


# Takes as an argument to LLM message content, returns a list of the fn result objects
def handle_function_calls(tool_call_message_content, document_retriever):
    tool_results = []

    for tool_call in tool_call_message_content:
        # Only process messages from the LLM that are function calls
        if tool_call["type"] != "tool_use":
            continue
        fn_id = tool_call["id"]
        fn_name = tool_call["name"]
        fn_args = tool_call["input"]
        fn_result = {
            "type": "tool_result",
            "tool_use_id": fn_id,
        }

        if fn_name == "query_food_recipe_vector_db":
            if "queries" not in fn_args:
                logger.error(
                    f"ERROR: Tried to call {fn_name} with invalid args {fn_args}, skipping.."
                )
                fn_result["content"] = ""
                fn_result["is_error"] = True
                tool_results.append(fn_result)
                continue

            logger.info(f"Model called {fn_name} with args {fn_args}")
            context_docs = handle_vector_db_queries(
                fn_args["queries"], document_retriever
            )
            context_str = format_docs(context_docs)
            fn_result["content"] = context_str
            tool_results.append(fn_result)

        elif fn_name == "google_web_search":
            if "queries" not in fn_args:
                logger.error(
                    f"ERROR: Tried to call {fn_name} with invalid args {fn_args}, skipping.."
                )
                fn_result["content"] = ""
                fn_result["is_error"] = True
                tool_results.append(fn_result)
                continue

            logger.info(f"Model called {fn_name} with args {fn_args}")
            search_results = handle_google_web_search(
                fn_args["queries"], google_search_api_key
            )
            search_results_str = json.dumps(search_results)
            fn_result["content"] = search_results_str
            tool_results.append(fn_result)

        else:
            logger.error(f"ERROR: Attempted call to unknown function {fn_name}")
            fn_result["content"] = ""
            fn_result["is_error"] = True
            tool_results.append(fn_result)

    return tool_results


"""
Example payload structure of response_body:

{'id': 'msg_bdrk_01REesjegNiLteurBoxW7pSt',
 'type': 'message',
 'role': 'assistant',
 'model': 'claude-3-sonnet-20240229',
 'content': [{'type': 'tool_use',
   'id': 'toolu_bdrk_01191W2FuAFTRoDqKKeJSmmn',
   'name': 'query_food_recipe_vector_db',
   'input': {'queries': ['thai food',
     'peanut free',
     'low carb',
     'not spicy']}}],
 'stop_reason': 'tool_use',
 'stop_sequence': None,
 'usage': {'input_tokens': 573, 'output_tokens': 52}}


Example payload structure of llm_message['content']:

[{'type': 'tool_use',
   'id': 'toolu_bdrk_01191W2FuAFTRoDqKKeJSmmn',
   'name': 'query_food_recipe_vector_db',
   'input': {'queries': ['thai food',
     'peanut free',
     'low carb',
     'not spicy']}}]
"""


# This function is the entry point to invoke the LLM with support for function calling
# parsing output, calling requested functions, sending output is handled here
def run_chat_loop(existing_chat_history, prompt, document_retriever, config):
    logger.info(f"[User]: {prompt}")

    response_body, llm_message, chat_history = message_handler(
        existing_chat_history=existing_chat_history, prompt=prompt, config=config
    )

    # The model wants to call tools, call them, provide response, repeat until content is generated
    fn_calls = []
    while response_body["stop_reason"] == "tool_use":
        fn_calls.extend(response_body["content"])
        fn_results = handle_function_calls(
            tool_call_message_content=llm_message["content"],
            document_retriever=document_retriever,
        )

        # Send function results back to LLM as a new message with the existing chat history
        response_body, llm_message, chat_history = message_handler(
            existing_chat_history=chat_history,
            prompt=fn_results,
            is_tool_message=True,
            config=config,
        )

    # The model is done calling tools, parse output and update chat
    # history with the models response
    model_text_output = llm_message["content"][0]["text"]
    logger.info(f"\n[Model]: {model_text_output}")

    return [model_text_output, chat_history, fn_calls]

def run_chat_loop_streaming(existing_chat_history, prompt, document_retriever, config):
    logger.info(f"[User]: {prompt}")

    messages = existing_chat_history
    messages.append(generate_message(prompt))
    logger.info("Messages are now: %s", messages)

    response_stream = query_bedrock_llm_streaming(messages, config)
    logger.info("Received response stream")

    accumulated_response = ""
    fn_calls = []

    for chunk in response_stream:
        logger.info("Processing chunk: %s", chunk)
        
        # Extract bytes from the nested dictionary
        if 'chunk' in chunk and 'bytes' in chunk['chunk']:
            chunk_bytes = chunk['chunk']['bytes']
            chunk_str = chunk_bytes.decode('utf-8')
        else:
            logger.warning("Skipping non-string/byte chunk")
            continue  # Skip if chunk is neither bytes nor string

        accumulated_response += chunk_str
        try:
            response_body = json.loads(accumulated_response)
            logger.info("Parsed response body: %s", response_body)
            
            # Handle different types of responses
            if 'type' in response_body and response_body['type'] == 'message_start':
                yield f"data: {json.dumps(response_body)}\n\n"
                accumulated_response = ""  # Reset after processing

            elif 'type' in response_body and response_body['type'] == 'message_delta':
                yield f"data: {json.dumps(response_body)}\n\n"
                accumulated_response = ""  # Reset after processing

            elif 'type' in response_body and response_body['type'] == 'message_stop':
                yield f"data: {json.dumps(response_body)}\n\n"
                accumulated_response = ""  # Reset after processing

            elif 'stop_reason' in response_body and response_body["stop_reason"] == "tool_use":
                fn_calls.extend(response_body["content"])
                fn_results = handle_function_calls(
                    tool_call_message_content=response_body["content"],
                    document_retriever=document_retriever,
                )

                response_body, llm_message, messages = message_handler(
                    existing_chat_history=messages,
                    prompt=fn_results,
                    is_tool_message=True,
                    config=config,
                )
                accumulated_response = ""  # Reset after processing
                yield f"data: {json.dumps(response_body)}\n\n"
                
            else:
                yield f"data: {json.dumps(response_body)}\n\n"
                accumulated_response = ""  # Reset after processing

        except json.JSONDecodeError:
            logger.warning("JSONDecodeError, waiting for more chunks")
            # Wait for more chunks to form a complete JSON
            continue
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            raise