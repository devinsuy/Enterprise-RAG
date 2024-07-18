import os
import logging

from constants import (DOCUMENT_CONTENT_DESCRIPTION, METADATA_FIELD_INFO,
                       SELF_QUERY_API, SELF_QUERY_MODEL, COARSE_SEARCH_KWARGS, RERANKER_TOP_N)
from llm.prompts import self_query_sys_prompt
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_community.vectorstores import Qdrant
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_core.runnables import RunnableMap, RunnablePassthrough

logger = logging.getLogger(__name__)
self_query_llm = None
fine_retriever = None
embedding_model = None


def intialize_reranker(base_retriever):
    reranker_model = HuggingFaceCrossEncoder(
        model_name="BAAI/bge-reranker-base")
    compressor = CrossEncoderReranker(model=reranker_model, top_n=RERANKER_TOP_N)
    reranker_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=base_retriever
    )
    return reranker_retriever

def initialize_chain_models():
    global embedding_model

    logger.info("Initializing retrieval models")
    embedding_model = HuggingFaceEmbeddings(
        model_name="multi-qa-mpnet-base-dot-v1")

    if SELF_QUERY_API == "OpenAI":
        self_query_llm = ChatOpenAI(
            model=SELF_QUERY_MODEL,
            temperature=0,
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
        )
    elif SELF_QUERY_API == "Azure":
        self_query_llm = AzureChatOpenAI(
            openai_api_version="2024-06-01",
            azure_deployment="capstone_gpt4o",
            openai_api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
            azure_endpoint="https://capstone1.openai.azure.com/",
        )
    else:
        raise ValueError("Invalid SELF_QUERY_API config - Set in constants.py\n"
                         "\t'OpenAI' or 'Azure'")
    logger.info(f"Found openAI credentials in environmental variables\n"
                f"Using {SELF_QUERY_API} for self_query_llm")

    reranker_model = HuggingFaceCrossEncoder(
        model_name="BAAI/bge-reranker-base")

    fine_search = CrossEncoderReranker(model=reranker_model, top_n=1)

    return self_query_llm, fine_search

def filtered_qdrant_store(documents=[]):
    # dependent on embedding_model global variable
    logger.info(f"intermediate qdrant store of {len(documents)} documents instantiated")
    filtered_qdrant_store = Qdrant.from_documents(documents,
        embedding_model,
        location=":memory:",
    )
    return filtered_qdrant_store

def self_query_message_prompt(user_prompt):
    string = f"user: {user_prompt}"
    message = self_query_sys_prompt + string
    return message

def self_query_wrapper(dict):
    # dependent on global variable self_query_llm
    self_query_retriever = SelfQueryRetriever.from_llm(
        self_query_llm, filtered_qdrant_store(dict['documents']), DOCUMENT_CONTENT_DESCRIPTION, METADATA_FIELD_INFO, verbose=True
    )
    documents = self_query_retriever.invoke(self_query_message_prompt(dict['query']))
    logger.info(f"Self query with LLM returned {len(documents)} documents out of {COARSE_SEARCH_KWARGS['k']} documents from coarse search")
    logger.info(f"Titles: {[doc.metadata['name'] for doc in documents]}")
    return {"documents": documents,
            "query": dict['query']}

def fine_search_wrapper(dict):
    # Expects chained pass of dict {query: "", documents: ""}
    # dependent on global variable fine_retriever
    if dict['documents'] == []:
        logger.info("No documents provided to fine-search. Passing empty list to bedrock llm")
        return ['']

    documents_found = fine_retriever.compress_documents(query=dict['query'],
                                   documents=dict['documents'])
    logger.info(f"Document returned: {[doc.metadata['name'] for doc in documents_found]}")

    return documents_found


def initialize_retrieval_chain(retriever):
    global self_query_llm
    global fine_retriever
    self_query_llm, fine_retriever = initialize_chain_models()
    retrieval_chain = (
            RunnableMap(
                {"documents": retriever,
                 "query": RunnablePassthrough()}
            )
            | self_query_wrapper
            | fine_search_wrapper
    )
    logger.info("Retrieval chain created")
    return retrieval_chain