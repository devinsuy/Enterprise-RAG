import json
import logging

import boto3
from constants import MODEL_ID, RETRIEVER
from data_utils import (format_docs, handle_vector_db_queries,
                        initialize_vector_db)
from retrieval_utils import initialize_retrieval_chain, intialize_reranker

from .message_utils import generate_message, generate_tool_message
from .prompts import baseline_sys_prompt
from .tools import recipe_db_query_tool

logger = logging.getLogger(__name__)

# Avoid implicit initialization, leads to race conditions with main.py importing this
document_retriever = None
bedrock_client = None


def init_llm_handler():
    global document_retriever
    global bedrock_client
    if RETRIEVER == "self_query_chain":
        logger.info("Retriever selected: retrieval_chain")
        coarse_retriever = initialize_vector_db()
        document_retriever = initialize_retrieval_chain(coarse_retriever)

    elif RETRIEVER == "reranker":
        logger.info("Retriever in use: reranker")
        coarse_retriever = initialize_vector_db()
        document_retriever = intialize_reranker(coarse_retriever)

    elif RETRIEVER == "coarse":
        logger.info("Retriever in use: coarse")
        document_retriever = initialize_vector_db()

    else:
        raise ValueError(
            "Invalid retriever selected - In constants.py set RETRIEVER"
            "to one of the following:\n"
            "\t'coarse', 'reranker', or 'self_query_chain'"
        )

    bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")


def query_bedrock_llm(messages):
    response = bedrock_client.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",  # This is required to use chat style messages object
                "system": baseline_sys_prompt,
                "messages": messages,
                "max_tokens": 3000,
                "tools": [recipe_db_query_tool],
                # This config forces the model to always call the recipe db query tool atleast once
                # https://docs.anthropic.com/en/docs/build-with-claude/tool-use#controlling-claudes-output
                # "tool_choice": {
                #     "type": "tool",
                #     "name": recipe_db_query_tool['name']
                # },
                # TODO: TUNE THESE VALUES
                "temperature": 0.1,
                "top_p": 0.9,
            }
        ),
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


def message_handler(existing_chat_history, prompt, is_tool_message=False):
    # Fn results is an array of tool response objects
    # message structure needs to reflect that
    if is_tool_message:
        user_message = generate_tool_message(prompt)
    else:
        user_message = generate_message(prompt)
    existing_chat_history.append(user_message)

    # Parse the response content
    response_body = query_bedrock_llm(existing_chat_history)
    llm_message = {"role": response_body["role"], "content": response_body["content"]}

    # Add the response message to the chat history
    existing_chat_history.append(llm_message)

    return [response_body, llm_message, existing_chat_history]


# Takes as an argument to LLM message content, returns a list of the fn result objects
def handle_function_calls(tool_call_message_content):
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

            model_msg = f"Model called {fn_name} with args {fn_args}"
            logger.info(model_msg)
            context_docs = handle_vector_db_queries(
                fn_args["queries"], document_retriever
            )
            context_str = format_docs(context_docs)
            fn_result["content"] = context_str
            tool_results.append(fn_result)

        # TODO: handle web search invocation here

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
def run_chat_loop(existing_chat_history, prompt):
    logger.info(f"[User]: {prompt}")

    response_body, llm_message, chat_history = message_handler(
        existing_chat_history=existing_chat_history, prompt=prompt
    )

    # The model wants to call tools, call them, provide response, repeat until content is generated
    fn_calls = []
    while response_body["stop_reason"] == "tool_use":
        fn_calls.extend(response_body["content"])
        fn_results = handle_function_calls(
            tool_call_message_content=llm_message["content"]
        )

        # Send function results back to LLM as a new message with the existing chat history
        response_body, llm_message, chat_history = message_handler(
            existing_chat_history=chat_history, prompt=fn_results, is_tool_message=True
        )

    # The model is done calling tools, parse output and update chat
    # history with the models response
    model_text_output = llm_message["content"][0]["text"]
    logger.info(f"\n[Model]: {model_text_output}")

    return [model_text_output, chat_history, fn_calls]
