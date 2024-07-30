import os
import json
import shutil

def process_json_file(input_filepath, output_filepath):
    with open(input_filepath, 'r') as file:
        data = json.load(file)
    
    processed_data = {}
    for key, value in data.items():
        if key.startswith("Entry_"):
            entry_data = value[1]  
            processed_data[key] = {
                "Query_Question_No": entry_data["Query_Question_No"],
                "Query_Question": entry_data["Query_Question"],
                "top_p": entry_data["top_p"],
                "top_k": entry_data["top_k"],
                "temperature": entry_data["temperature"],
                "max_tokens": entry_data["max_tokens"],
                "system_prompt": "\nYou are a helpful assistant and expert in cooking recipes.\n\nBefore answering, follow these requirements:\n\n- Always make at least one call to query_food_recipe_vector_db to retrieve the relevant context of recipes and ingredients to generate an informed and high-quality response to the user prompt, specifically for retrieving recipes, ingredients, preparation steps, and related metadata.\n\n- NEVER exceed a MAXIMUM of 3 calls to the query_food_recipe_vector_db function.\n\n- Analyze the user's requirements and NEVER provide a recipe that violates ANY of the user's requirements.\n\n- In your final response, NEVER include any XML tags with information about your thoughts. It is okay to include XML and analysis text in any message except your final one with the recipes and instructions.\n\nProvide a response to the user prompt about food with recommended recipes and instructions.\n",
                "retriever": entry_data["retriever"],
                "coarse_search_type": entry_data["coarse_search_type"],
                "coarse_top_k": entry_data["coarse_top_k"],
                "coarse_lambda": entry_data["coarse_lambda"],
                "reranker_top_n": entry_data["reranker_top_n"],
                "coarse_fetch_k": entry_data["coarse_fetch_k"],
                "self_query_api": entry_data["self_query_api"],
                "self_query_model": entry_data["self_query_model"],
                "Query_Response": entry_data["Query_Response"]
            }
    
    with open(output_filepath, 'w') as file:
        json.dump(processed_data, file, indent=4)

def main():
    input_folder = '.' 
    output_folder = os.path.join(input_folder, 'processed_files')

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            input_filepath = os.path.join(input_folder, filename)
            output_filepath = os.path.join(output_folder, filename)
            process_json_file(input_filepath, output_filepath)

    print("Processing complete. Processed files are saved in 'processed_files' folder.")

if __name__ == "__main__":
    main()
