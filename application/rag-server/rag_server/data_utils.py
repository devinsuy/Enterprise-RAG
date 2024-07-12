import json
import logging
import os

import boto3
import pandas as pd
from constants import BUCKET_NAME, DOWNLOAD_PATH, FILE_KEY
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant

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
    return df


def create_documents(df):
    df_copy = df.copy(deep=True)
    df = df.dropna(subset=["AggregatedRating"])
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


def initialize_vector_db():
    # Use this when developing to more quickly load
    # to avoid waiting for all 500,000+ documents
    # documents = initialize_documents(max_document_count=100)

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
        location=":memory:",
    )
    retriever = store.as_retriever()
    logger.info(f"Successfully initialized document db with {len(documents)} documents")

    return retriever


# Executes a list of queries and returns a list of document results
def handle_vector_db_queries(queries, retriever):
    context_docs = []
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
