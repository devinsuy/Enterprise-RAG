import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError, as_completed

import requests
from bs4 import BeautifulSoup

from constants import GCP_CSE_ID, NUM_SEARCH_RESULTS, WEB_MAX_CONTENT_LENGTH

logger = logging.getLogger(__name__)

FETCH_URL_LIMIT = 3  # Limit the number of URLs to fetch per search result


# Given a URL, fetch the page's text content. We truncate the website content
# to provide context of the site but without exceeding the model context window
# without truncation we quickly encounter server errors from bedrock
def get_page_content(url):
    logger.info(f"Fetching page content for URL: {url}")
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract all text content from the page
        text_content = soup.get_text(separator="\n")

        # Truncate content to a maximum length
        if len(text_content) > WEB_MAX_CONTENT_LENGTH:
            text_content = text_content[:WEB_MAX_CONTENT_LENGTH]

        return text_content
    except requests.exceptions.RequestException as e:
        logger.error(f'Failed to fetch page content for URL "{url}": {e}')
        return ""


# Executes a list of queries using the Google Custom Search API and returns a list of search results.
# Returns:
# A dictionary where each query maps to a list of search results. Each search result contains the title and snippet.
def handle_google_web_search(
    queries, api_key, cse_id=GCP_CSE_ID, num_results=NUM_SEARCH_RESULTS
):
    # Ensure queries is a list of strings
    if isinstance(queries, str):
        queries = [queries]
    elif not isinstance(queries, list) or not all(isinstance(q, str) for q in queries):
        logger.error("Queries should be a list of strings.")
        return {}

    # The base URL for the Google Custom Search API
    api_url = "https://www.googleapis.com/customsearch/v1"

    all_search_results = {}

    def fetch_search_results(query):
        logger.info(f"Fetching Google search results for query: {query}")
        params = {"key": api_key, "cx": cse_id, "q": query, "num": num_results}
        try:
            response = requests.get(api_url, params=params, timeout=3)
            response.raise_for_status()
            return query, response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching search results for query {query}: {e}")
            return query, None

    def fetch_page_content(item):
        search_result_url = item.get("link")
        page_content = get_page_content(search_result_url)
        return {
            "title": item.get("title"),
            "snippet": item.get("snippet"),
            "page_content": page_content,
        }

    with ThreadPoolExecutor() as executor:
        # Fetch search results in parallel
        future_to_query = {
            executor.submit(fetch_search_results, query): query for query in queries
        }

        for future in as_completed(future_to_query):
            try:
                query, search_results = future.result(timeout=5)
            except TimeoutError:
                logger.error(
                    f"Timeout occurred while fetching search results for query {query}"
                )
                all_search_results[query] = []
                continue
            except Exception as e:
                logger.error(
                    f"Unexpected error while fetching search results for query {query}: {e}"
                )
                all_search_results[query] = []
                continue

            if search_results is None:
                all_search_results[query] = []
                continue

            # Fetch page content in parallel for each search result item, limit to the first 3 URLs
            items = search_results.get("items", [])[:FETCH_URL_LIMIT]
            future_to_item = {
                executor.submit(fetch_page_content, item): item for item in items
            }
            results = []
            for future in as_completed(future_to_item):
                try:
                    result = future.result(timeout=5)
                except TimeoutError:
                    logger.error(f"Timeout occurred while fetching page content")
                    result = {"title": "Timeout", "snippet": "", "page_content": ""}
                except Exception as e:
                    logger.error(f"Unexpected error while fetching page content: {e}")
                    result = {"title": "Error", "snippet": "", "page_content": ""}
                results.append(result)

            all_search_results[query] = results

    return all_search_results
