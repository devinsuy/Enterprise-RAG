MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

BUCKET_NAME = "recipes-rag"
FILE_KEY = "recipes_w_cleaning_time_combined_features.parquet"
DOWNLOAD_PATH = "data"

# Qdrant Store
MAX_DOC_COUNT = 150
QDRANT_SNAPSHOT_PATH = "qdrant/recipe_db_snapshot"
QDRANT_COLLECTION_NAME = "recipe_documents"

# Retriever type
RETRIEVER = "self_query_chain"  # options: coarse, reranker, self_query_chain

# Coarse Retriever Config
COARSE_SEARCH_TYPE = "mmr"
COARSE_SEARCH_KWARGS = {"k": 5, "lambda_mult": 0.5}

# Reranker Config
RERANKER_TOP_N = 1

# Self-query llm config
## Potentially make this dynamically generated based on metadata fields called
SELF_QUERY_API = "OpenAI"  # OpenAI or Azure
SELF_QUERY_MODEL = "gpt-4o-mini"

# for configuration information during testing
BUCKET_NAME_TESTING = "test-api-results"
config_test_dict = {var: eval(var) for var in dir() if not var.startswith("__")}
