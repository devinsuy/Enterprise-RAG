baseline_sys_prompt = """
You are a helpful assistant and expert in cooking recipes.

Before answering, always make at least one call to query_food_recipe_vector_db
to retrieve the relevant context of recipes and ingredients to generate an informed
and high-quality response to the user prompt but NEVER exceed a MAXIMUM of 
3 calls to the query_food_recipe_vector_db function.

Provide a response to the user prompt about food with recommended recipes and instructions.
"""

test_query_1 = """
I enjoy asian fusion food and I am a vegetarian. 
Give me one recipe with ingredients and instructions
"""

test_query_2 = """
I have a peanut allergy but I like thai food. 
I also don't enjoy spicy food much, and want a meal with low carbs. 
Give a recipe with ingredients and instructions
"""

test_query_3 = """
Suggest a low-carb breakfast recipe that includes eggs and spinach, 
can be prepared in under 20 minutes, 
and is suitable for a keto diet.
"""

test_query_4 = """
Suggest a healthy dinner recipe for two people that includes fish, 
is under 500 calories per serving, 
and can be made in less than 40 minutes.
"""

test_query_5 = """
I am on a ketogenic diet and need a dinner recipe that is dairy-free, 
low in sodium, and takes less than an hour to cook.
"""

test_query_6 = """
I'm looking for a pescatarian main course that is low in saturated fat, 
uses Asian flavors, and can be prepared in under 45 minutes.
"""

test_query_7 = """
I need a diabetic-friendly, vegan breakfast recipe that is gluten-free, 
nut-free, and low in cholesterol, but also rich in omega-3 fatty acids 
and can be prepared the night before.
"""

test_query_8 = """
I am following a strict paleo diet and need a lunch recipe that is dairy-free, 
gluten-free, low in carbs, and low in sodium. Additionally, it should be rich in antioxidants, 
and can be made in under 30 minutes with minimal cooking equipment.
"""