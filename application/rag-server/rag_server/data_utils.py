import logging
import os
import uuid

import boto3
import pandas as pd
from langchain.docstore.document import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient, models

from constants import (BUCKET_NAME, COARSE_LAMBDA, COARSE_SEARCH_TYPE,
                       COARSE_TOP_K, DOWNLOAD_PATH, EMBEDDING_MODEL_ID,
                       FILE_KEY, QDRANT_COLLECTION_NAME, QDRANT_HOST_URL,
                       QDRANT_SNAPSHOT_URL)

logger = logging.getLogger(__name__)


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

    return documents


def initialize_vector_db(
    snapshot_url=QDRANT_SNAPSHOT_URL,
    qdrant_url=QDRANT_HOST_URL,
    recreate_db=False,
    needs_init=False,
):
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
        retriever = store.as_retriever(
            search_type=COARSE_SEARCH_TYPE,
            search_kwargs={"k": COARSE_TOP_K, "lambda_mult": COARSE_LAMBDA},
        )
        return [store, retriever]

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

    # Generate an embedding to determine the vector size
    sample_vector = embedding_model.embed_query(documents[0].page_content)
    vector_size = len(sample_vector)

    qdrant_client = QdrantClient(
        url=qdrant_url, timeout=300
    )  # Allow up to 5 minutes before failing slow requests

    # Create a collection with dynamically determined vector size
    qdrant_client.create_collection(
        collection_name=QDRANT_COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=vector_size, distance=models.Distance.COSINE
        ),
    )

    # Prepare data for batch upload
    batch_size = 1000
    for i in range(0, len(documents), batch_size):
        batch_docs = documents[i : i + batch_size]
        ids, vectors, payloads = [], [], []
        for j, doc in enumerate(batch_docs):
            ids.append(str(uuid.uuid4()))  # Use UUIDs to ensure valid point IDs
            vectors.append(embedding_model.embed_query(doc.page_content))
            payloads.append(doc.metadata)

        # Batch upload documents
        qdrant_client.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            points=models.Batch(ids=ids, vectors=vectors, payloads=payloads),
        )
        logger.info(
            f"Uploaded batch {i // batch_size + 1} of {len(documents) // batch_size + 1}"
        )

    # NOTE TO SELF:
    # If Snapshot times out, try upping timeout, if all fails, check docker logs, to see if creation succeeded still
    # if so, manually copy it out and upload to S3, then restart server without recreate_db flag set to restore it
    qdrant_client.create_snapshot(collection_name=QDRANT_COLLECTION_NAME)

    store = Qdrant(
        client=qdrant_client,
        collection_name=QDRANT_COLLECTION_NAME,
        embeddings=embedding_model,
    )
    retriever = store.as_retriever(
        search_type=COARSE_SEARCH_TYPE,
        search_kwargs={"k": COARSE_TOP_K, "lambda_mult": COARSE_LAMBDA},
    )
    logger.info(f"Successfully initialized document db with {len(documents)} documents")

    return [store, retriever]


# def restore_db_instance(snapshot_path=QDRANT_SNAPSHOT_URL):
#     logger.info("Loading embedding model")
#     embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_ID)

#     global store
#     global retriever

#     # Restore snapshot
#     qdrant_client = QdrantClient(path=snapshot_path)

#     store = Qdrant(
#         client=qdrant_client,
#         collection_name=QDRANT_COLLECTION_NAME,
#         embeddings=embedding_model,
#     )
#     retriever = store.as_retriever(
#         search_type=COARSE_SEARCH_TYPE,
#         search_kwargs={"k": COARSE_TOP_K, "lambda_mult": COARSE_LAMBDA},
#     )
#     num_docs = qdrant_client.count(
#         collection_name=QDRANT_COLLECTION_NAME, exact=True
#     ).count
#     logger.info(
#         f"Successfully restored document db snapshot from {snapshot_path} with {num_docs} documents"
#     )

#     return retriever


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
    retriever = store.as_retriever(
        search_type=COARSE_SEARCH_TYPE,
        search_kwargs={"k": COARSE_TOP_K, "lambda_mult": COARSE_LAMBDA},
    )
    num_docs = qdrant_client.count(collection_name=collection_name, exact=True).count
    logger.info(
        f"Successfully restored document db snapshot from {snapshot_url} with {num_docs} documents"
    )

    return [store, retriever]


def handle_vector_db_queries(queries, retriever):
    context_docs = []
    if isinstance(queries, str):
        queries = [queries]
    for query in queries:
        query_results = retriever.invoke(query)
        context_docs.extend(query_results)

    return context_docs


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
