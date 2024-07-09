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
    documents = []
    for _index, row in df.iterrows():
        metadata = {
            "recipe_id": (
                str(row["RecipeId"])
                if not pd.isna(row["RecipeId"])
                else "No ID Available"
            ),
            "name": (
                str(row["Name"]) if not pd.isna(row["Name"]) else "No Name Available"
            ),
            "cook_time": (
                str(row["CookTime"])
                if not pd.isna(row["CookTime"])
                else "No Cook Time Available"
            ),
            "prep_time": (
                str(row["PrepTime"])
                if not pd.isna(row["PrepTime"])
                else "No Prep Time Available"
            ),
            "total_time": (
                str(row["TotalTime"])
                if not pd.isna(row["TotalTime"])
                else "No Total Time Available"
            ),
            "recipe_category": (
                str(row["RecipeCategory"])
                if not pd.isna(row["RecipeCategory"])
                else "No Category Available"
            ),
            "keywords": (
                str(row["Keywords"])
                if not pd.isna(row["Keywords"]).all()
                else "No Keywords Available"
            ),
            "aggregated_rating": (
                str(row["AggregatedRating"])
                if not pd.isna(row["AggregatedRating"])
                else "No Rating Available"
            ),
            "review_count": (
                str(row["ReviewCount"])
                if not pd.isna(row["ReviewCount"])
                else "No Reviews Available"
            ),
            "calories": (
                str(row["Calories"])
                if not pd.isna(row["Calories"])
                else "No Calories Information Available"
            ),
            "fat_content": (
                str(row["FatContent"])
                if not pd.isna(row["FatContent"])
                else "No Fat Content Available"
            ),
            "saturated_fat_content": (
                str(row["SaturatedFatContent"])
                if not pd.isna(row["SaturatedFatContent"])
                else "No Saturated Fat Content Available"
            ),
            "cholesterol_content": (
                str(row["CholesterolContent"])
                if not pd.isna(row["CholesterolContent"])
                else "No Cholesterol Content Available"
            ),
            "sodium_content": (
                str(row["SodiumContent"])
                if not pd.isna(row["SodiumContent"])
                else "No Sodium Content Available"
            ),
            "carbohydrate_content": (
                str(row["CarbohydrateContent"])
                if not pd.isna(row["CarbohydrateContent"])
                else "No Carbohydrate Content Available"
            ),
            "sugar_content": (
                str(row["SugarContent"])
                if not pd.isna(row["SugarContent"])
                else "No Sugar Content Available"
            ),
            "protein_content": (
                str(row["ProteinContent"])
                if not pd.isna(row["ProteinContent"])
                else "No Protein Content Available"
            ),
            "recipe_servings": (
                str(row["RecipeServings"])
                if not pd.isna(row["RecipeServings"])
                else "No Servings Information Available"
            ),
            "recipe_yield": (
                str(row["RecipeYield"])
                if not pd.isna(row["RecipeYield"])
                else "No Yield Information Available"
            ),
        }

        # Use Combined_Features_Clean for the document content
        text = str(row["Combined_Features_Clean"])
        doc = Document(page_content=text, metadata=metadata)
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
    documents = initialize_documents(max_document_count=1000)

    # documents = initialize_documents()

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
    for doc in docs:
        formatted_docs.append(f"Metadata: {doc.metadata}\n")
    content = "\n\n".join(formatted_docs)

    return content
