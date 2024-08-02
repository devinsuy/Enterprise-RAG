import json
import logging

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from api_types import ConverseToolResultStatus
from constants import MODEL_ID
from data_utils import format_docs, get_secret, handle_vector_db_queries
from google_search import handle_google_web_search

from .message_utils import (generate_converse_message,
                            generate_converse_tool_message, generate_message,
                            generate_tool_message)
from .tools import (converse_google_web_search_tool,
                    converse_recipe_db_query_tool, google_web_search_tool,
                    recipe_db_query_tool)

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


# https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use-examples.html
def converse_msg_stream_handler(messages, config):
    response = bedrock_client.converse_stream(
        modelId=MODEL_ID,
        messages=messages,
        system=[{"text": str(config.system_prompt)}],
        inferenceConfig={
            "temperature": float(config.temperature),
            "topP": float(config.top_p),
            "maxTokens": int(config.max_tokens),
        },
        additionalModelRequestFields={"top_k": int(config.top_k)},
        toolConfig={
            "tools": [converse_recipe_db_query_tool, converse_google_web_search_tool]
        },
    )

    stop_reason = ""
    message = {"role": "assistant", "content": []}
    text = ""
    tool_use = {}

    for chunk in response["stream"]:
        if "messageStart" in chunk:
            message["role"] = chunk["messageStart"]["role"]
        elif "contentBlockStart" in chunk:
            tool = chunk["contentBlockStart"]["start"]["toolUse"]
            tool_use = {"toolUseId": tool["toolUseId"], "name": tool["name"]}
        elif "contentBlockDelta" in chunk:
            delta = chunk["contentBlockDelta"]["delta"]
            if "toolUse" in delta:
                if "input" not in tool_use:
                    tool_use["input"] = ""
                tool_use["input"] += delta["toolUse"]["input"]
            elif "text" in delta:
                text += delta["text"]
                yield None, {"role": "assistant", "content": [{"text": text}]}
        elif "contentBlockStop" in chunk:
            if "input" in tool_use:
                tool_use["input"] = json.loads(tool_use["input"])
                message["content"].append({"toolUse": tool_use})
                tool_use = {}
            else:
                message["content"].append({"text": text})
                text = ""
        elif "messageStop" in chunk:
            stop_reason = chunk["messageStop"]["stopReason"]

    yield stop_reason, message


# Messages are created for each accumulated version streamed from the model,
# strip them out and only keep the final completed message
def dedupe_streamed_messages(messages):
    # Check if messages never repeat the same role more than once before alternating
    repeated_role = False
    for i in range(1, len(messages)):
        if messages[i]["role"] == messages[i - 1]["role"]:
            repeated_role = True
            break

    # If no repeated roles, return messages as is
    if not repeated_role:
        return messages

    # Process messages to strip out redundant assistant messages
    processed_messages = []
    last_assistant_message = None

    for message in messages:
        if message["role"] == "assistant":
            last_assistant_message = message
        else:
            if last_assistant_message:
                processed_messages.append(last_assistant_message)
                last_assistant_message = None
            processed_messages.append(message)

    # Append the last assistant message if exists
    if last_assistant_message:
        processed_messages.append(last_assistant_message)

    return processed_messages


def run_chat_loop_streaming(existing_chat_history, prompt, document_retriever, config):
    try:
        messages = existing_chat_history
        messages.append(generate_converse_message(prompt))

        accumulated_text = ""
        for stop_reason, message in converse_msg_stream_handler(messages, config):
            if message:
                if message["content"] and "text" in message["content"][-1]:
                    accumulated_text += message["content"][-1]["text"]
                messages.append(message)
                yield message

            while stop_reason == "tool_use":
                for content in message["content"]:
                    if "toolUse" not in content:
                        continue

                    tool_use = content["toolUse"]
                    fn_id = tool_use["toolUseId"]
                    fn_name = tool_use["name"]
                    fn_args = tool_use["input"]
                    fn_result = {"toolUseId": fn_id}

                    if fn_name == "query_food_recipe_vector_db":
                        if "queries" not in fn_args:
                            logger.error(
                                f"ERROR: Tried to call {fn_name} with invalid args {fn_args}, skipping..."
                            )
                            fn_result["content"] = []
                            fn_result["status"] = "error"
                            continue

                        logger.info(f"Model called {fn_name} with args {fn_args}")
                        context_docs = handle_vector_db_queries(
                            fn_args["queries"], document_retriever
                        )
                        context_str = format_docs(context_docs)
                        fn_result["content"] = [{"text": context_str}]
                        fn_result["status"] = "success"

                    elif fn_name == "google_web_search":
                        if "queries" not in fn_args:
                            logger.error(
                                f"ERROR: Tried to call {fn_name} with invalid args {fn_args}, skipping..."
                            )
                            fn_result["content"] = []
                            fn_result["status"] = "error"
                            continue

                        logger.info(f"Model called {fn_name} with args {fn_args}")

                        search_results = handle_google_web_search(
                            fn_args["queries"], google_search_api_key
                        )
                        search_results_str = json.dumps(search_results)
                        fn_result["content"] = [{"text": search_results_str}]
                        fn_result["status"] = "success"

                    else:
                        logger.error(
                            f"ERROR: Attempted call to unknown function {fn_name}"
                        )
                        fn_result["content"] = []
                        fn_result["status"] = "error"

                    tool_result_message = generate_converse_tool_message(fn_result)
                    messages.append(tool_result_message)

                # Sanitize messages before sending
                messages = dedupe_streamed_messages(messages)

                for stop_reason, message in converse_msg_stream_handler(
                    messages, config
                ):
                    if message:
                        if message["content"] and "text" in message["content"][-1]:
                            accumulated_text += message["content"][-1]["text"]
                        messages.append(message)
                        yield message
    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        yield {"error": str(message)}

    else:
        yield {"info": "Finished streaming messages with model."}
