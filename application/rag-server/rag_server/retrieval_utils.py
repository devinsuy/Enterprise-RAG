import os
import logging

from constants import (DOCUMENT_CONTENT_DESCRIPTION, METADATA_FIELD_INFO,
                       SELF_QUERY_MODEL, COARSE_SEARCH_KWARGS)
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_community.vectorstores import Qdrant
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_core.runnables import RunnableMap, RunnablePassthrough

logger = logging.getLogger(__name__)

def initialize_retrieval_models():
    global self_query_llm
    global fine_search
    global embedding_model

    logger.info("Initializing retrieval models")
    embedding_model = HuggingFaceEmbeddings(
        model_name="multi-qa-mpnet-base-dot-v1")
    self_query_llm = ChatOpenAI(
        model=SELF_QUERY_MODEL,
        temperature=0,
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
    )
    logger.info("Found openAI credentials in environmental variables")

    reranker_model = HuggingFaceCrossEncoder(
        model_name="BAAI/bge-reranker-base")
    fine_search = CrossEncoderReranker(model=reranker_model, top_n=1)

    return self_query_llm, fine_search

def filtered_qdrant_store(documents=[]):
    # dependent on embedding_model global variable
    filtered_qdrant_store = Qdrant.from_documents(documents,
        embedding_model,
        location=":memory:",
    )
    return filtered_qdrant_store

def self_query_message_prompt(user_prompt):
    f"""
system: You are a helpful assistant and expert in cooking recipes.

You are evaluating for consistency of the user query.
Please retrieve documents that DO NOT violate dietary restrictions, allergies, 
or any requirements dictated by the user.

user: {user_prompt}
"""

def self_query_wrapper(dict):
    print('in self_query_wrapper')
    # dependent on global variable self_query_llm
    self_query_retriever = SelfQueryRetriever.from_llm(
        self_query_llm, filtered_qdrant_store(dict['documents']), DOCUMENT_CONTENT_DESCRIPTION, METADATA_FIELD_INFO, verbose=True
    )
    documents = self_query_retriever.invoke(self_query_message_prompt(dict['query']))
    logger.info(f"Self query with LLM returned {len(documents)} documents out of {COARSE_SEARCH_KWARGS['k']} documents from coarse search")
    return {"documents": documents,
            "query": dict['query']}

def fine_search_wrapper(dict):
    # Expects chained pass of dict {query: "", documents: ""}
    # dependent on global variable fine_search
    return fine_search.compress_documents(query=dict['query'], documents=dict['documents'])


def initialize_retrieval_chain(retriever, self_query_llm, fine_search):
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