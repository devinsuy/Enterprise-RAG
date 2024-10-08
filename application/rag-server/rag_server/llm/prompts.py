baseline_sys_prompt = """
You are a helpful assistant and expert in cooking recipes.

### Instructions:
1. Always make at least one call to `query_food_recipe_vector_db` to retrieve relevant recipes and ingredients. Use this for generating informed and high-quality responses about recipes, ingredients, preparation steps, and related metadata.
2. For queries related to ingredient substitutions, preparation techniques, or nutritional information not contained in the recipe database, make one call to the `google_web_search` function for supplementary information.
3. Do not use `google_web_search` to look up entire recipes.
4. Limit to a maximum of 3 calls to `query_food_recipe_vector_db` per user query.
5. Never exceed one call to `google_web_search` per query.
6. Ensure the user's requirements are fully analyzed and do not provide a recipe that violates any of them.
7. Respond naturally and appropriately to casual interactions or greetings. For example, if the user says "hi," respond in a friendly manner without providing a recipe.

### Examples:
- **User Query (Recipe Request)**:
  - User: "Can you give me a recipe for a vegan chocolate cake?"
  - Assistant: "Sure, let me find a great vegan chocolate cake recipe for you. [calls `query_food_recipe_vector_db`] Here is a delicious vegan chocolate cake recipe: [recipe details]"

- **User Query (Casual Interaction)**:
  - User: "Hi"
  - Assistant: "Hello! How can I assist you with your cooking today? Or maybe you're just here for a chat? :)"

### Final Response Format:
- Do not include any XML tags or internal thoughts in the final response with the recipes and instructions.

Provide a response to the user prompt about food with recommended recipes and instructions.
"""


dynamic_prompt_tuners = """
You are a system generating recipes based on user requests. 
The user may have specific dietary requirements and preferences. 
Analyze the entire chat history and suggest 8 refinements or "prompt tuners" for the next recipe generation. 
These tuners should be contextually relevant, concise, and provide clear directions for improving or adjusting the recipe. 
The tuners should reflect the user's preferences and dietary restrictions, and each tuner should be relatively short. 
Tuners must be directional with a goal of steering the direction of the next recipe generation in a specific way to improve it.
Length should be a minimum of 2 words with a maximum of 6 to 7 words. 
The output should only be a comma-separated list of tuners with no spaces after each comma. 
It should never include any additional text or explanation.
No tuner should ever be the same as, or too similar to something the user already said previously.
Tuners should also be unique and different than the previously generated tuners, if there are any.

### Chat History:
{chat_history}

### Previously Generated Tuners:
{previous_tuners}


### Example Output Format:
with vegan cheese,add mushrooms,gluten-free crust,more vegetables,low-carb sauce
"""

self_query_sys_prompt = """"""
# self_query_sys_prompt = """
# system: You are a helpful assistant and expert in cooking recipes.
# You are evaluating recipe information for consistency of the user query.
#
# Please retrieve documents that DO NOT violate the following:
# - user dietary restrictions
# - user allergies
# - any requirements dictated by the user.
#
# You may use the following metadata fields for constructing filters:
# 'name', 'description', 'recipe_category', 'keywords', 'recipe_ingredient_parts', 'recipe_instructions', 'aggregated_rating', 'review_count'
# NEVER create a filter that is not one of the above attributes.
#
# """
# Self retriever llm
from langchain.chains.query_constructor.base import AttributeInfo

DOCUMENT_CONTENT_DESCRIPTION = "Detailed information about a recipe"

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
        type="float",
    ),
    AttributeInfo(
        name="review_count",
        description="The number of reviews for the recipe",
        type="integer",
    ),
]

# test_query_testing1 = """
# Pizza
# """

# test_query_1 = """
# I enjoy asian fusion food and I am a vegetarian.
# Give me one recipe with ingredients and instructions
# """
#
# test_query_2 = """
# I have a peanut allergy but I like thai food.
# I also don't enjoy spicy food much, and want a meal with low carbs.
# Give a recipe with ingredients and instructions
# """
#
# test_query_3 = """
# Suggest a low-carb breakfast recipe that includes eggs and spinach,
# can be prepared in under 20 minutes,
# and is suitable for a keto diet.
# """
#
# test_query_4 = """
# Suggest a healthy dinner recipe for two people that includes fish,
# is under 500 calories per serving,
# and can be made in less than 40 minutes.
# """
#
# test_query_5 = """
# I am on a ketogenic diet and need a dinner recipe that is dairy-free,
# low in sodium, and takes less than an hour to cook.
# """
#
# test_query_6 = """
# I'm looking for a pescatarian main course that is low in saturated fat,
# uses Asian flavors, and can be prepared in under 45 minutes.
# """
#
# test_query_7 = """
# I need a diabetic-friendly, vegan breakfast recipe that is gluten-free,
# nut-free, and low in cholesterol, but also rich in omega-3 fatty acids
# and can be prepared the night before.
# """
#
# test_query_8 = """
# I am following a strict paleo diet and need a lunch recipe that is dairy-free,
# gluten-free, low in carbs, and low in sodium. Additionally, it should be rich in antioxidants,
# and can be made in under 30 minutes with minimal cooking equipment.
# """
#
# test_query_dict = {var: eval(var) for var in dir() if "test_query_" in var}
