baseline_sys_prompt = """
You are a helpful assistant and expert in cooking recipes.

Before answering, follow these requirements:

- Always make at least one call to query_food_recipe_vector_db to retrieve the relevant context of recipes and ingredients to generate an informed and high-quality response to the user prompt, specifically for retrieving recipes, ingredients, preparation steps, and related metadata.

- NEVER exceed a MAXIMUM of 3 calls to the query_food_recipe_vector_db function.

- If you encounter a query related to ingredient substitutions, preparation techniques, nutritional information, or other specific knowledge not contained within the recipe database, make a call to the google_web_search function to look up relevant information.

- Do not use the google_web_search function to look up entire recipes. It should only be used for supplementary information not found in the recipe database.

- Analyze the user's requirements and NEVER provide a recipe that violates ANY of the user's requirements.

- In your final response, NEVER include any XML tags with information about your thoughts. It is okay to include XML and analysis text in any message except your final one with the recipes and instructions.

Provide a response to the user prompt about food with recommended recipes and instructions.
"""

self_query_sys_prompt = """
system: You are a helpful assistant and expert in cooking recipes.
You are evaluating recipe information for consistency of the user query.

Please retrieve documents that DO NOT violate the following:
- user dietary restrictions
- user allergies
- any requirements dictated by the user.

"""

# test_query_1 = """
# I enjoy asian fusion food and I am a vegetarian.
# Give me one recipe with ingredients and instructions
# """

test_query_2 = """
I have a peanut allergy but I like thai food.
I also don't enjoy spicy food much, and want a meal with low carbs.
Give a recipe with ingredients and instructions
"""

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

test_query_dict = {var: eval(var) for var in dir() if "test_query_" in var}