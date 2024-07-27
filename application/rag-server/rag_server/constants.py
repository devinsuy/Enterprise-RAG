MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"
EMBEDDING_MODEL_ID = "multi-qa-mpnet-base-dot-v1"
RERANKER_MODEL_ID = "BAAI/bge-reranker-base"

BUCKET_NAME = "recipes-rag"
FILE_KEY = "recipes_w_cleaning_time_combined_features.parquet"
DOWNLOAD_PATH = "data"

# Qdrant Store
MAX_DOC_COUNT = 150
QDRANT_HOST_URL = "http://localhost:6333"
QDRANT_SNAPSHOT_URL = "https://public-recipe-db-snapshot.s3.amazonaws.com/recipe_documents-5791562930133689-2024-07-27-08-30-54.snapshot"
QDRANT_COLLECTION_NAME = "recipe_documents"
QDRANT_S3_PATH = "qdrant/recipe_db_snapshot"

# Retriever type
RETRIEVER = "self_query_chain"  # options: coarse, reranker, self_query_chain

# Coarse Retriever Config
COARSE_SEARCH_TYPE = "similarity"
COARSE_TOP_K = 5
COARSE_LAMBDA = 0.5

# Reranker Config
RERANKER_TOP_N = 1

# Self-query llm config
## Potentially make this dynamically generated based on metadata fields called
SELF_QUERY_API = "OpenAI"  # OpenAI or Azure
SELF_QUERY_MODEL = "gpt-4o-mini"

# for configuration information during testing
BUCKET_NAME_TESTING = "test-api-results"
config_test_dict = {var: eval(var) for var in dir() if not var.startswith("__")}
