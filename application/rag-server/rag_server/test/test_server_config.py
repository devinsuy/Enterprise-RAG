import json
import random
from concurrent.futures import ThreadPoolExecutor
from time import sleep

import requests

endpoint = "https://api.scraps2scrumptious.com/v1/chat"
headers = {
    "Authorization": "1ffdb6d4ca73edd45497c1defd4902d06bc0f17066207ff9499ccf1f80528255",  # REMOVED
    "Content-Type": "application/json",
}

possible_configurations = {
    "top_p": [0.7, 0.8, 0.9],
    "top_k": [20, 30, 40],
    "temperature": [0.5, 0.7, 0.9],
    "max_tokens": [1000, 2000, 3000],
    "retriever": ["coarse", "reranker", "self_query_chain"],
    "coarse_search_type": ["similarity", "mmr"],
    "coarse_top_k": [3, 5, 7],
    "coarse_lambda": [0.3, 0.5, 0.7],
    "reranker_top_n": [1, 2, 3],
    "coarse_fetch_k": [50, 100, 150],
    "self_query_api": ["OpenAI"],
    "self_query_model": ["gpt-4o-mini"],
}


# Create random configurations with correct types
def create_random_config():
    config = {
        "top_p": float(random.choice(possible_configurations["top_p"])),
        "top_k": int(random.choice(possible_configurations["top_k"])),
        "temperature": float(random.choice(possible_configurations["temperature"])),
        "max_tokens": int(random.choice(possible_configurations["max_tokens"])),
        "retriever": random.choice(possible_configurations["retriever"]),
        "coarse_search_type": random.choice(
            possible_configurations["coarse_search_type"]
        ),
        "coarse_top_k": int(random.choice(possible_configurations["coarse_top_k"])),
        "coarse_lambda": float(random.choice(possible_configurations["coarse_lambda"])),
        "reranker_top_n": int(random.choice(possible_configurations["reranker_top_n"])),
        "coarse_fetch_k": int(random.choice(possible_configurations["coarse_fetch_k"])),
        "self_query_api": random.choice(possible_configurations["self_query_api"]),
        "self_query_model": random.choice(possible_configurations["self_query_model"]),
    }
    return config


# Prepare the payload
def create_payload():
    config = create_random_config()
    payload = {
        "existing_chat_history": [],
        "prompt": "I am cooking dinner for 5 today. Some of my family is vegetarian. I want to make a healthy fusion dish.",
        "config": config,
    }
    return json.dumps(payload)


# Function to make a single request
def make_request():
    payload = create_payload()
    response = requests.post(endpoint, headers=headers, data=payload)
    if response.status_code == 200:
        print(f"Request succeeded: {response.json()}")
    else:
        print(f"Request failed: {response.status_code} - {response.text}")


# Function to run multiple requests concurrently
def run_requests_concurrently(num_requests):
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(make_request) for _ in range(num_requests)]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Request failed with exception: {e}")


# Run the requests
if __name__ == "__main__":
    run_requests_concurrently(30)
