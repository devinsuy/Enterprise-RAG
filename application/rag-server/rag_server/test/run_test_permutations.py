# pip install aiohttp
# pip install pydantic python-dotenv

import asyncio
import itertools
import json
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
api_key = "1ffdb6d4ca73edd45497c1defd4902d06bc0f17066207ff9499ccf1f80528255"  # REDACTED
headers = {"Authorization": api_key, "Content-Type": "application/json"}


# Function to make a request
async def make_request(session, payload):
    async with session.post(api_endpoint, headers=headers, json=payload) as response:
        result = await response.json()
        return result


# Function to handle a single permutation
async def handle_permutation(session, permutation):
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
    print(f"Sending request with payload: {payload}")
    # result = await make_request(session, payload)
    # print(f"Received response: {result}")
    await asyncio.sleep(1)  # Add short delay


# Main function to run all permutations with concurrency
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        semaphore = asyncio.Semaphore(3)  # Limit to 3 concurrent requests

        for permutation in permutations:
            await semaphore.acquire()
            task = asyncio.create_task(handle_permutation(session, permutation))
            task.add_done_callback(lambda t: semaphore.release())
            tasks.append(task)

        await asyncio.gather(*tasks)


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
