import concurrent.futures
import json
import logging
import os

import boto3
import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient

from constants import (BUCKET_NAME, DOWNLOAD_PATH, EMBEDDING_MODEL_ID,
                       FILE_KEY, QDRANT_COLLECTION_NAME, QDRANT_HOST_URL,
                       QDRANT_SNAPSHOT_URL)

logger = logging.getLogger(__name__)

# Ensure AWS creds always load before bedrock client is instantiated
load_dotenv()

secrets_client = boto3.client("secretsmanager", region_name="us-east-1")


# Util to fetch key value secrets from AWS Secrets Manager
def get_secret(secret_name, is_json=False):
    try:
        get_secret_value_response = secrets_client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        raise e

    secret = get_secret_value_response["SecretString"]

    if is_json:
        return json.loads(secret)
    else:
        return secret


def download_and_load_data_if_not_exists(bucket_name, file_key, download_path):
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    file_path = os.path.join(download_path, file_key)

    if not os.path.exists(file_path):
        s3 = boto3.client("s3")
        s3.download_file(bucket_name, file_key, file_path)

    df = pd.read_parquet(file_path)
    df = df.dropna(subset=["AggregatedRating"])
    df = df.dropna(subset=["ReviewCount"])
    return df


def download_s3_folder(bucket_name, s3_folder, local_dir):
    logger.info(
        f"Downloading remote directory from bucket {bucket_name}: {s3_folder} to local path: {local_dir}"
    )
    s3 = boto3.client("s3")

    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
        logger.info(f"Created local directory: {local_dir}")

    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket_name, Prefix=s3_folder):
        if "Contents" in page:
            for obj in page["Contents"]:
                key = obj["Key"]
                relative_path = key[len(s3_folder) :].lstrip("/")
                local_path = os.path.join(local_dir, relative_path)
                local_subdir = os.path.dirname(local_path)
                if not os.path.exists(local_subdir):
                    os.makedirs(local_subdir)
                    logger.info(f"Created subdirectory: {local_subdir}")
                try:
                    s3.download_file(bucket_name, key, local_path)
                    logger.info(f"Downloaded {key} to {local_path}")
                except PermissionError as e:
                    logger.error(f"PermissionError: {e}. Cannot write to {local_path}")


def create_documents(df):
    df_copy = df.copy(deep=True)
    df_copy = df_copy.astype({"AggregatedRating": float, "ReviewCount": int})
    df_copy = df_copy.fillna("")
    df_copy = df_copy.astype(str)

    documents = []
    for _index, row in df_copy.iterrows():
        metadata = {
            "name": row["Name"] if row["Name"] else "No Name Available",
            "description": (
                row["Description"] if row["Description"] else "No Description Available"
            ),
            "recipe_category": (
                row["RecipeCategory"]
                if row["RecipeCategory"]
                else "No Category Available"
            ),
            "keywords": (
                row["Keywords_string"]
                if row["Keywords_string"]
                else "No Keywords Available"
            ),
            "recipe_ingredient_parts": (
                row["RecipeIngredientParts"]
                if row["RecipeIngredientParts"]
                else "No Recipe Ingredient Parts Available"
            ),
            "recipe_instructions": (
                row["RecipeInstructions"]
                if row["RecipeInstructions"]
                else "No Recipe Instructions Available"
            ),
            "aggregated_rating": (
                row["AggregatedRating"]
                if row["AggregatedRating"]
                else "No Rating Available"
            ),
            "review_count": (
                row["ReviewCount"] if row["ReviewCount"] else "No Reviews Available"
            ),
        }

        content_field = (
            row["Combined_Features"]
            if row["Combined_Features"]
            else "No Content Available"
        )
        doc = Document(page_content=content_field, metadata=metadata)

        if len(doc.page_content) > 0:
            documents.append(doc)

    return documents


def initialize_documents(max_document_count=None):
    logger.info("Initializing recipes data")
    df = download_and_load_data_if_not_exists(BUCKET_NAME, FILE_KEY, DOWNLOAD_PATH)
    if max_document_count is not None:
        df = df.sample(n=max_document_count)

    documents = create_documents(df)
    logger.info(f"Successfully created {len(documents)} documents")
    logger.info(f"First doc: {documents[0]}")
    logger.info(f"First doc: {documents[0].page_content}")

    return documents


def initialize_vector_db(
    snapshot_url=QDRANT_SNAPSHOT_URL,
    qdrant_url=QDRANT_HOST_URL,
    recreate_db=False,
    needs_init=False,
):
    # return create_db_instance()
    # No creation or reloading necessary, just return a reference
    if needs_init == False:
        logger.info("Loading embedding model")
        embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_ID)
        logger.info("DB is already running, restoring client and retriever")
        qdrant_client = QdrantClient(
            url=qdrant_url, timeout=300
        )  # Allow up to 5 minutes before failing slow requests
        store = Qdrant(
            client=qdrant_client,
            collection_name=QDRANT_COLLECTION_NAME,
            embeddings=embedding_model,
        )
        return store

    # Recreate or restore from snapshot
    if recreate_db:
        logger.info("Recreating vector DB instance from scratch")
        return create_db_instance()
    else:
        logger.info(f"Restoring vector DB from snapshot at: {snapshot_url}")
        return restore_db_instance_from_url(snapshot_url)


def create_db_instance(qdrant_url=QDRANT_HOST_URL):
    documents = initialize_documents()
    logger.info("Loading embedding model")
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_ID)

    store = Qdrant.from_documents(
        documents,
        embedding_model,
        url=qdrant_url,
        prefer_grpc=False,
        collection_name=QDRANT_COLLECTION_NAME,
    )
    logger.info(f"Successfully initialized document db with {len(documents)} documents")

    return store


def restore_db_instance_from_url(
    snapshot_url, collection_name=QDRANT_COLLECTION_NAME, qdrant_url=QDRANT_HOST_URL
):
    logger.info("Loading embedding model")
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_ID)
    qdrant_client = QdrantClient(
        url=qdrant_url, timeout=300
    )  # Allow up to 5 minutes before failing slow requests

    # Restore the snapshot from the URL
    qdrant_client.recover_snapshot(
        collection_name=collection_name, location=snapshot_url
    )
    store = Qdrant(
        client=qdrant_client,
        collection_name=collection_name,
        embeddings=embedding_model,
    )
    num_docs = qdrant_client.count(collection_name=collection_name, exact=True).count
    logger.info(
        f"Successfully restored document db snapshot from {snapshot_url} with {num_docs} documents"
    )

    return store


def handle_vector_db_queries(queries, retriever):
    context_docs = {}

    # Ensure queries is a list of strings
    if isinstance(queries, str):
        queries = [queries]
    elif not isinstance(queries, list) or not all(isinstance(q, str) for q in queries):
        logger.error("Queries should be a list of strings.")
        return []

    def fetch_query_results(query):
        return retriever.invoke(query)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_query = {
            executor.submit(fetch_query_results, query): query for query in queries
        }
        for future in concurrent.futures.as_completed(future_to_query):
            query = future_to_query[future]
            try:
                query_results = future.result()
                context_docs[query] = query_results
            except Exception as e:
                logger.error(f"Error fetching query results for query {query}: {e}")

    return context_docs


def format_docs(docs):
    formatted_docs = []
    excluded_columns = ["name", "recipe_category", "description"]

    for query, documents in docs.items():
        query_header = f"Query: {query}\n"
        formatted_docs.append(query_header)

        for doc in documents:
            doc_content = doc.page_content
            metadata_content = "\n".join(
                f"{key}: {value}"
                for key, value in doc.metadata.items()
                if key not in excluded_columns and value != "No Data Available"
            )
            formatted_doc = f"{doc_content}\n\nMetadata:\n{metadata_content}"
            formatted_docs.append(formatted_doc)

        formatted_docs.append("\n---\n")  # Adding a separator between different queries

    content = "\n".join(formatted_docs)
    return content
