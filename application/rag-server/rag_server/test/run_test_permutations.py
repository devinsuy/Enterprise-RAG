import asyncio
import itertools
import json
import logging
import traceback
from logging.handlers import RotatingFileHandler

import aiohttp

# Configuration options
temperatures = [0.1, 0.5, 1.0]
top_ks = [2, 10]
top_ps = [0.1, 0.9]
retrievers = ["coarse", "reranker", "self_query_chain"]
use_gatekeeper_queries = [True, False]


# Generate all permutations of the configurations
all_permutations = list(
    itertools.product(temperatures, top_ks, top_ps, retrievers, use_gatekeeper_queries)
)


# API endpoint and headers
api_endpoint = "http://0.0.0.0:8000/v1/recipes/test_queries"
api_key = ""  # REDACTED
headers = {"Authorization": api_key, "Content-Type": "application/json"}

# Configure logging
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
log_file = "test_permutations.log"

file_handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=3)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
stream_handler.setLevel(logging.INFO)

logging.basicConfig(level=logging.INFO, handlers=[file_handler, stream_handler])
logger = logging.getLogger(__name__)

# Test and Gatekeeper queries
test_queries = [
    "I enjoy asian fusion food and I am a vegetarian. Give me one recipe with ingredients and instructions.",
    "I have a peanut allergy but I like thai food. I also don't enjoy spicy food much, and want a meal with low carbs. Give a recipe with ingredients and instructions.",
    "Suggest a low-carb breakfast recipe that includes eggs and spinach, can be prepared in under 20 minutes, and is suitable for a keto diet.",
    "Suggest a healthy dinner recipe for two people that includes fish, is under 500 calories per serving, and can be made in less than 40 minutes.",
    "I am on a ketogenic diet and need a dinner recipe that is dairy-free, low in sodium, and takes less than an hour to cook.",
    "I'm looking for a pescatarian main course that is low in saturated fat, uses Asian flavors, and can be prepared in under 45 minutes.",
    "I need a diabetic-friendly, vegan breakfast recipe that is gluten-free, nut-free, and low in cholesterol, but also rich in omega-3 fatty acids and can be prepared the night before.",
    "I am following a strict paleo diet and need a lunch recipe that is dairy-free, gluten-free, low in carbs, and low in sodium. Additionally, it should be rich in antioxidants, and can be made in under 30 minutes with minimal cooking equipment.",
    "I am following a legionnairs diet and need a dinner recipe. Provide a recipe that can be made under 45 minutes.",
    "I need a kid-friendly, nut-free snack recipe that is also low in sugar and can be prepared in under 25 minutes for my daughter and son.",
    "I am on a heart-healthy diet and need a lunch recipe that is low in saturated fat, high in omega-3 fatty acids, and can be prepared in less than 40 minutes for a family of four.",
    "I am allergic to shellfish and soy. I need a vegetarian Japanese food recipe high in protein and fiber and can be prepared in less than 30 minutes.",
    "I am lactose intolerant and need a dessert recipe that is dairy-free, gluten-free, and low in sugar, but still tastes rich and creamy.",
    "Suggest a high-fiber, low-calorie lunch recipe that includes beans, is vegetarian, and can be prepared in less than 25 minutes.",
    "Suggest a Middle Eastern vegan lunch recipe that is rich in protein, includes chickpeas, and can be prepared in less than 35 minutes.",
]

gate_keeper_queries = [
    "I am allergic to peanuts. Can you suggest a dessert recipe for me?",
    "I have a shellfish allergy. Please provide a dinner recipe.",
    "I follow a vegan diet. Can you give me a breakfast recipe?",
    "I need a gluten-free lunch recipe. What can you suggest?",
    "I don't eat dairy products. Can you provide a pasta recipe?",
    "I avoid sugar. Please suggest a dessert recipe without sugar.",
    "I am allergic to both nuts and dairy. Can you recommend a snack recipe?",
    "I need a gluten-free and vegan dinner recipe. What do you have?",
    "I don't eat beef for religious reasons. Can you provide a main course recipe?",
    "I only eat halal food. Can you give me a recipe for a special occasion?",
    "I am on a low-carb diet. Can you suggest a low-carb dinner recipe?",
    "I need a low-sodium breakfast recipe. What can you recommend?",
    "My child is allergic to eggs. Can you suggest a kid-friendly snack recipe?",
    "I need a lunch recipe for my child who doesn't eat nuts or dairy.",
    "I don't have any tomatoes. Can you provide a salad recipe without tomatoes?",
    "I am out of eggs. Can you give me a baking recipe that doesn't require eggs?",
    "I have diabetes. Can you suggest a dessert recipe suitable for me?",
    "I have high cholesterol. Can you provide a heart-healthy dinner recipe?",
    "Please give me a recipe for chicken soup, but it must not contain any garlic.",
    "I am looking for a recipe for a cake, but it should not include any artificial sweeteners.",
    "I am allergic to peanuts. Can you suggest a peanut butter cookie recipe?",
    "I follow a vegan diet but also want a recipe with chicken. Can you provide one?",
    "I need a gluten-free pasta recipe, but please include wheat flour.",
    "I avoid sugar and dairy, but can you suggest a sweet and creamy dessert?",
]


async def make_request(session, payload, identifier, retries=3):
    for attempt in range(retries):
        try:
            async with session.post(
                api_endpoint, headers=headers, json=payload
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    logger.error(
                        f"Failed request [ID: {identifier}] with payload: {payload} - response: {response.status} - {response.reason}"
                    )
        except aiohttp.ClientError as e:
            logger.error(f"Request failed [ID: {identifier}]: {e}")
            if attempt < retries - 1:
                await asyncio.sleep(2**attempt)  # Exponential backoff
        except Exception as e:
            logger.error(
                f"Unexpected error [ID: {identifier}]: {e}\n{traceback.format_exc()}"
            )
            if attempt < retries - 1:
                await asyncio.sleep(2**attempt)  # Exponential backoff
    return None


async def handle_permutation(session, permutation, semaphore):
    temperature, top_k, top_p, retriever, gatekeeper_query = permutation
    config = {
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "retriever": retriever,
    }

    queries = gate_keeper_queries if gatekeeper_query else test_queries

    existing_state = {}
    for i, query in enumerate(queries):
        payload = {
            "test_queries": [query],
            "use_gatekeeper_queries": gatekeeper_query,
            "config": config,
            "existing_state": existing_state,
        }
        identifier = f"{permutation}_{i+1}"
        logger.info(f"Sending request [ID: {identifier}] with payload: {payload}")
        async with semaphore:
            result = await make_request(session, payload, identifier)
            if result:
                logger.info(f"Received response [ID: {identifier}]: {result}")
                existing_state = result.get("state", {})
            else:
                logger.error(f"Failed permutation [ID: {identifier}]")
                break


async def main():
    max_concurrent_requests = 5  # Adjust this value based on your needs
    semaphore = asyncio.Semaphore(max_concurrent_requests)
    async with aiohttp.ClientSession() as session:
        tasks = [
            handle_permutation(session, perm, semaphore) for perm in all_permutations
        ]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
