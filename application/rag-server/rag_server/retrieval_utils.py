import logging
import os

from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_community.vectorstores import Qdrant
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import AzureChatOpenAI, ChatOpenAI

from constants import COARSE_TOP_K, EMBEDDING_MODEL_ID, RERANKER_MODEL_ID
from llm.prompts import (DOCUMENT_CONTENT_DESCRIPTION, METADATA_FIELD_INFO,
                         self_query_sys_prompt)

logger = logging.getLogger(__name__)
self_query_llm = None
fine_retriever = None
embedding_model = None


def intialize_reranker(base_retriever, config):
    reranker_model = HuggingFaceCrossEncoder(model_name=RERANKER_MODEL_ID)
    compressor = CrossEncoderReranker(model=reranker_model, top_n=config.reranker_top_n)
    reranker_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=base_retriever
    )
    return reranker_retriever


def initialize_chain_models(config):
    global embedding_model

    logger.info("Initializing retrieval models")
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_ID)

    if config.self_query_api == "OpenAI":
        self_query_llm = ChatOpenAI(
            model=config.self_query_model,
            temperature=0,
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            max_retries=3,
        )
    elif config.self_query_api == "Azure":
        self_query_llm = AzureChatOpenAI(
            openai_api_version="2024-06-01",
            azure_deployment="capstone_gpt4o",
            openai_api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
            azure_endpoint="https://capstone1.openai.azure.com/",
        )
    else:
        raise ValueError(
            "Invalid SELF_QUERY_API config - Set in constants.py\n"
            "\t'OpenAI' or 'Azure'"
        )
    logger.info(
        f"Found openAI credentials in environmental variables\n"
        f"Using {config.self_query_api} for self_query_llm"
    )

    reranker_model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")

    fine_search = CrossEncoderReranker(model=reranker_model, top_n=1)

    return self_query_llm, fine_search


def filtered_qdrant_store(documents=[]):
    # dependent on embedding_model global variable
    logger.info(f"intermediate qdrant store of {len(documents)} documents instantiated")
    filtered_qdrant_store = Qdrant.from_documents(
        documents,
        embedding_model,
        location=":memory:",
    )
    return filtered_qdrant_store


def self_query_message_prompt(user_prompt):
    user_prompt = f"user: {user_prompt}"
    message = [self_query_sys_prompt + user_prompt]
    return message


def self_query_wrapper(dict):
    # dependent on global variable self_query_llm
    prompt = self_query_message_prompt(dict["query"])
    temp_store = filtered_qdrant_store(dict["documents"])

    # been having an issue where the self_query_llm makes up metadata fields and attributes
    try:
        self_query_retriever = SelfQueryRetriever.from_llm(
            self_query_llm,
            temp_store,
            document_contents=DOCUMENT_CONTENT_DESCRIPTION,
            metadata_field_info=METADATA_FIELD_INFO,
            use_original_query=False,
            enable_limit=False,
            verbose=True,
        )
        documents = self_query_retriever.invoke(prompt)
    except Exception as e:
        logger.error(f"Error while invoking SelfQueryRetriever: {e}")
        logger.warning(f"Forcing SelfQueryRetriever to NOT generate filters")
        self_query_retriever_no_meta = SelfQueryRetriever.from_llm(
            self_query_llm,
            temp_store,
            document_contents=DOCUMENT_CONTENT_DESCRIPTION,
            metadata_field_info=[],
            use_original_query=False,
            enable_limit=False,
            verbose=True,
        )
        documents = self_query_retriever_no_meta.invoke(prompt)

    logger.info(
        f"Coarse search: {COARSE_TOP_K} docs, Self query: {len(documents)} docs"
    )

    # Log the first document to inspect the structure
    if documents:
        logger.info(f"First document structure: {documents[0]}")

    # Log document titles with error handling
    titles = []
    for doc in documents:
        try:
            titles.append(doc.metadata["name"])
        except KeyError:
            logger.warning(f"Document {doc} is missing 'name' in metadata")

    logger.info(f"Titles: {titles}")
    return {"documents": documents, "query": dict["query"]}


# # Additionally, you can add a log to inspect all documents if needed
#     logger.info(f"All documents structure: {documents}")


def fine_search_wrapper(dict):
    # Expects chained pass of dict {query: "", documents: ""}
    # dependent on global variable fine_retriever
    if dict["documents"] == []:
        logger.info(
            "No documents provided to fine-search. Passing empty list to bedrock llm"
        )
        return []

    documents_found = fine_retriever.compress_documents(
        query=dict["query"], documents=dict["documents"]
    )
    logger.info(
        f"Retrieval complete - document returned: {[doc.metadata['name'] for doc in documents_found]}"
    )

    return documents_found


def initialize_retrieval_chain(retriever, config):
    global self_query_llm
    global fine_retriever
    self_query_llm, fine_retriever = initialize_chain_models(config)
    retrieval_chain = (
        RunnableMap({"documents": retriever, "query": RunnablePassthrough()})
        | self_query_wrapper
        | fine_search_wrapper
    )
    logger.info("Retrieval chain created")
    return retrieval_chain
