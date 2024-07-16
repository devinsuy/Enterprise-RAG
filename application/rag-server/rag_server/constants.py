from langchain.chains.query_constructor.base import AttributeInfo

MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

BUCKET_NAME = "recipes-rag"
FILE_KEY = "recipes_w_cleaning_time_combined_features.parquet"
DOWNLOAD_PATH = "data"

# Store Retrieval Config
COARSE_SEARCH_TYPE = "mmr"
COARSE_SEARCH_KWARGS = {"k": 20, 'lambda_mult': 0.5}


# Self-query llm config
## Potentially make this dynamically generated based on metadata fields called
SELF_QUERY_MODEL = 'gpt-4o'
METADATA_FIELD_INFO = [
    AttributeInfo(
        name="name",
        description="The name of the recipe",
        type="string",
    ),
    AttributeInfo(
        name="description",
        description="A brief description of the recipe",
        type="string",
    ),
    AttributeInfo(
        name="recipe_category",
        description="The category of the recipe, such as 'Quick Breads', 'Desserts', etc.",
        type="string",
    ),
    AttributeInfo(
        name="keywords",
        description="Keywords associated with the recipe",
        type="string",
    ),
    AttributeInfo(
        name="recipe_ingredient_parts",
        description="The ingredients required for the recipe",
        type="string",
    ),
    AttributeInfo(
        name="recipe_instructions",
        description="The instructions to prepare the recipe",
        type="string",
    ),
    AttributeInfo(
        name="aggregated_rating",
        description="The aggregated rating for the recipe",
        type="string",
    ),
    AttributeInfo(
        name="review_count",
        description="The number of reviews for the recipe",
        type="string",
    ),
]

DOCUMENT_CONTENT_DESCRIPTION = "Detailed information about a recipe"
