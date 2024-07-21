import json
import logging
import os

import boto3
import pandas as pd
from constants import (BUCKET_NAME, COARSE_SEARCH_KWARGS, COARSE_SEARCH_TYPE,
                       DOWNLOAD_PATH, FILE_KEY, MAX_DOC_COUNT,
                       QDRANT_COLLECTION_NAME, QDRANT_SNAPSHOT_PATH)
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import Qdrant
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient

logger = logging.getLogger(__name__)
store = None
retriever = None


def init_data_utils():
    # Load environment variables from .env file
    load_dotenv()


# Load data from s3
def download_and_load_data_if_not_exists(bucket_name, file_key, download_path):
    # Ensure the directory exists
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    file_path = os.path.join(download_path, file_key)

    # Check if the file already exists, download it if needed
    if not os.path.exists(file_path):
        s3 = boto3.client("s3")
        s3.download_file(bucket_name, file_key, file_path)

    df = pd.read_parquet(file_path)
    df = df.dropna(subset=["AggregatedRating"])
    df = df.dropna(subset=["ReviewCount"])
    return df


def create_documents(df):
    df_copy = df.copy(deep=True)
    # df_copy = df_copy.dropna(subset=["AggregatedRating"])
    # df_copy = df_copy.dropna(subset=["ReviewCount"])
    df_copy = df_copy.astype({"AggregatedRating": float, "ReviewCount": int})

    df_copy = df_copy.fillna("")  # Convert NA values to empty strings
    df_copy = df_copy.astype(str)  # Cast all columns to string

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

        # List of fields to be included in the document content
        content_field = (
            row["Combined_Features"]
            if row["Combined_Features"]
            else "No Content Available"
        )

        # Create the document content using the combined features field
        doc = Document(page_content=content_field, metadata=metadata)

        # Skip documents without any content
        if len(doc.page_content) > 0:
            documents.append(doc)

    return documents


def initialize_documents(max_document_count=None):
    logger.info("Initializing recipes data")
    df = download_and_load_data_if_not_exists(BUCKET_NAME, FILE_KEY, DOWNLOAD_PATH)
    if max_document_count != None:
        df = df.sample(
            n=max_document_count
        )  # Reduce the number of rows by randomly sampling

    documents = create_documents(df)
    logger.info(f"Successfully created {len(documents)} documents")

    return documents


def initialize_vector_db(snapshot_path=QDRANT_SNAPSHOT_PATH):
    if not snapshot_path or not os.path.exists(snapshot_path):
        logger.info(
            f"No db snapshot found at {snapshot_path}, creating document database"
        )
        return create_db_instance(snapshot_path)
    else:
        logger.info(
            f"Found existing db snapshot at {snapshot_path}, restoring instance"
        )
        return restore_db_instance(snapshot_path)


# Create a db instance, computes embeddings and persists to disk
def create_db_instance(snapshot_path=QDRANT_SNAPSHOT_PATH):
    # Use this when developing to more quickly load
    # to avoid waiting for all 500,000+ documents
    # documents = initialize_documents(max_document_count=MAX_DOC_COUNT)
    documents = initialize_documents()

    logger.info("Loading embedding model")
    embedding_model = HuggingFaceEmbeddings(model_name="multi-qa-mpnet-base-dot-v1")

    # Update references
    global store
    global retriever

    logger.info("Initializing document db, this will take a while ...")
    store = Qdrant.from_documents(
        documents,
        embedding_model,
        path=QDRANT_SNAPSHOT_PATH,
        collection_name=QDRANT_COLLECTION_NAME,
    )
    retriever = store.as_retriever(
        search_type=COARSE_SEARCH_TYPE,
        search_kwargs={"k": COARSE_TOP_K, "lambda_mult": COARSE_LAMBDA},
    )
    logger.info(f"Successfully initialized document db with {len(documents)} documents")

    return retriever


# Reloads a vector db snapshot from disk to avoid
# recomputing document embeddings
def restore_db_instance(snapshot_path=QDRANT_SNAPSHOT_PATH):
    logger.info("Loading embedding model")
    embedding_model = HuggingFaceEmbeddings(model_name="multi-qa-mpnet-base-dot-v1")

    # Update references
    global store
    global retriever

    # Restore snapshot
    qdrant_client = QdrantClient(path=snapshot_path)

    store = Qdrant(
        client=qdrant_client,
        collection_name=QDRANT_COLLECTION_NAME,
        embeddings=embedding_model,
    )
    retriever = store.as_retriever(
        search_type=COARSE_SEARCH_TYPE, search_kwargs=COARSE_SEARCH_KWARGS
    )
    num_docs = qdrant_client.count(
        collection_name=QDRANT_COLLECTION_NAME, exact=True
    ).count
    logger.info(
        f"Successfully restored document db snapshot from {snapshot_path} with {num_docs} documents"
    )

    return retriever


# Executes a list of queries and returns a list of document results
def handle_vector_db_queries(queries, retriever):
    context_docs = []
    if isinstance(queries, str):
        queries = [queries]
    for query in queries:
        query_results = retriever.invoke(query)
        context_docs.extend(query_results)

    return context_docs


# Converts a list of document objects into a string with its metadata
def format_docs(docs):
    formatted_docs = []
    excluded_columns = ["name", "recipe_category", "description"]

    for doc in docs:
        doc_content = doc.page_content
        metadata_content = "\n".join(
            f"{key}: {value}"
            for key, value in doc.metadata.items()
            if key not in excluded_columns and value != "No Data Available"
        )
        formatted_doc = f"{doc_content}\n\nMetadata:\n{metadata_content}"
        formatted_docs.append(formatted_doc)

    content = "\n\n---\n\n".join(formatted_docs)
    return content
