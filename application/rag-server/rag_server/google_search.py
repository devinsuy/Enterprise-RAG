import logging

import requests
from bs4 import BeautifulSoup

from constants import GCP_CSE_ID, NUM_SEARCH_RESULTS

logger = logging.getLogger(__name__)


# Given a url fetch the page's text content
def get_page_content(url):
    logger.info(f"Fetching page content for url: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract all text content from the page
        text_content = soup.get_text(separator="\n")

        return text_content
    except requests.exceptions.RequestException as e:
        logger.error(f'Failed to fetch page content for url "{url}": {e}')
        return ""


"""
Executes a list of queries using the Google Custom Search API and returns a list of search results.

Returns:
A dictionary where each query maps to a list of search results. Each search result contains the title, and snippet.
"""


def handle_google_web_search(
    queries, api_key, cse_id=GCP_CSE_ID, num_results=NUM_SEARCH_RESULTS
):
    # The base URL for the Google Custom Search API
    api_url = "https://www.googleapis.com/customsearch/v1"

    all_search_results = {}

    for query in queries:
        logger.info(f"Fetching google search results for query: {query}")
        params = {"key": api_key, "cx": cse_id, "q": query, "num": num_results}
        response = requests.get(api_url, params=params)

        # Raise an exception if the request was unsuccessful
        response.raise_for_status()

        # Parse the JSON response
        search_results = response.json()

        # Extract the relevant information from the search results
        urls = [item.get("link") for item in search_results.get("items")]
        results = []
        for item in search_results.get("items", []):
            search_result_url = item.get("link")
            page_content = get_page_content(search_result_url)
            result = {
                "title": item.get("title"),
                "snippet": item.get("snippet"),
                "page_content": page_content,
            }
            results.append(result)

        # Map the query to its search results
        all_search_results[query] = results

    return all_search_results
