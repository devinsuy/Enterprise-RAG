# pip install aiohttp
# pip install pydantic python-dotenv

import asyncio
import itertools
import json
import logging
import time

import aiohttp

# Configuration options
temperatures = [0.1, 0.9]
top_ks = [2, 10]
top_ps = [0.1, 0.9]
retrievers = ["coarse", "reranker", "self_query_chain"]
use_gatekeeper_queries = [True, False]

# Generate all permutations of the configurations
permutations = list(
    itertools.product(temperatures, top_ks, top_ps, retrievers, use_gatekeeper_queries)
)

# API endpoint and headers
api_endpoint = "https://api.scraps2scrumptious.com/v1/recipes/test_queries"
api_key = ""  # REDACTED
headers = {"Authorization": api_key, "Content-Type": "application/json"}

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Function to make a request
async def make_request(session, payload):
    async with session.post(api_endpoint, headers=headers, json=payload) as response:
        if response.status != 200:
            logger.error(
                f"Failed request with payload: {payload} - response: {response}"
            )
        result = await response.json()
        return result


# Function to handle a single permutation
async def handle_permutation(session, semaphore, permutation):
    async with semaphore:
        temperature, top_k, top_p, retriever, gatekeeper_query = permutation
        payload = {
            "use_gatekeeper_queries": gatekeeper_query,
            "config": {
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "retriever": retriever,
            },
        }
        logger.info(f"Sending request with payload: {payload}")
        result = await make_request(session, payload)
        logger.info(f"Received response: {result}")
        await asyncio.sleep(1)  # Add short delay


# Main function to run all permutations with concurrency
async def main():
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(4)  # Limit to 4 concurrent requests

        tasks = [
            handle_permutation(session, semaphore, permutation)
            for permutation in permutations
        ]

        await asyncio.gather(*tasks)


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
