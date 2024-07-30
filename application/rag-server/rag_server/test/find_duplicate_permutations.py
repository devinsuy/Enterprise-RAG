import os
from collections import defaultdict

generated_files = [
"test_queries_results_gatekeeper_False_DocRetreiver.coarse_top_p_0.1_top_k_10_temp_0.1_07-29-22-43.json",
"test_queries_results_gatekeeper_False_DocRetreiver.coarse_top_p_0.1_top_k_10_temp_0.5_07-29-19-33.json",
"test_queries_results_gatekeeper_False_DocRetreiver.coarse_top_p_0.1_top_k_10_temp_1.0_07-29-19-36.json",
"test_queries_results_gatekeeper_False_DocRetreiver.coarse_top_p_0.1_top_k_2_temp_0.1_07-29-19-25.json",
"test_queries_results_gatekeeper_False_DocRetreiver.coarse_top_p_0.1_top_k_2_temp_0.5_07-29-19-32.json",
"test_queries_results_gatekeeper_False_DocRetreiver.coarse_top_p_0.1_top_k_2_temp_1.0_07-29-19-34.json",
"test_queries_results_gatekeeper_False_DocRetreiver.coarse_top_p_0.9_top_k_10_temp_0.1_07-29-19-31.json",
"test_queries_results_gatekeeper_False_DocRetreiver.coarse_top_p_0.9_top_k_10_temp_0.5_07-29-19-34.json",
"test_queries_results_gatekeeper_False_DocRetreiver.coarse_top_p_0.9_top_k_10_temp_1.0_07-29-19-37.json",
"test_queries_results_gatekeeper_False_DocRetreiver.coarse_top_p_0.9_top_k_2_temp_0.1_07-29-19-27.json",
"test_queries_results_gatekeeper_False_DocRetreiver.coarse_top_p_0.9_top_k_2_temp_0.5_07-29-19-33.json",
"test_queries_results_gatekeeper_False_DocRetreiver.coarse_top_p_0.9_top_k_2_temp_1.0_07-29-19-35.json",
"test_queries_results_gatekeeper_False_DocRetreiver.reranker_top_p_0.1_top_k_10_temp_0.1_07-29-19-30.json",
"test_queries_results_gatekeeper_False_DocRetreiver.reranker_top_p_0.1_top_k_10_temp_0.5_07-29-19-33.json",
"test_queries_results_gatekeeper_False_DocRetreiver.reranker_top_p_0.1_top_k_10_temp_1.0_07-29-19-36.json",
"test_queries_results_gatekeeper_False_DocRetreiver.reranker_top_p_0.1_top_k_2_temp_0.1_07-29-19-26.json",
"test_queries_results_gatekeeper_False_DocRetreiver.reranker_top_p_0.1_top_k_2_temp_0.5_07-29-19-31.json",
"test_queries_results_gatekeeper_False_DocRetreiver.reranker_top_p_0.1_top_k_2_temp_1.0_07-29-19-34.json",
"test_queries_results_gatekeeper_False_DocRetreiver.reranker_top_p_0.9_top_k_10_temp_0.1_07-29-19-31.json",
"test_queries_results_gatekeeper_False_DocRetreiver.reranker_top_p_0.9_top_k_10_temp_0.5_07-29-19-34.json",
"test_queries_results_gatekeeper_False_DocRetreiver.reranker_top_p_0.9_top_k_10_temp_1.0_07-29-19-37.json",
"test_queries_results_gatekeeper_False_DocRetreiver.reranker_top_p_0.9_top_k_2_temp_0.1_07-29-19-29.json",
"test_queries_results_gatekeeper_False_DocRetreiver.reranker_top_p_0.9_top_k_2_temp_0.5_07-29-19-32.json",
"test_queries_results_gatekeeper_False_DocRetreiver.reranker_top_p_0.9_top_k_2_temp_1.0_07-29-19-36.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.1_top_k_10_temp_0.1_07-29-19-31.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.1_top_k_10_temp_0.1_07-29-22-43.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.1_top_k_10_temp_0.5_07-29-19-33.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.1_top_k_10_temp_0.5_07-29-22-44.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.1_top_k_10_temp_1.0_07-29-19-36.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.1_top_k_10_temp_1.0_07-29-22-45.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.1_top_k_2_temp_0.1_07-29-19-28.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.1_top_k_2_temp_0.1_07-29-22-42.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.1_top_k_2_temp_0.5_07-29-19-32.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.1_top_k_2_temp_0.5_07-29-22-44.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.1_top_k_2_temp_1.0_07-29-19-35.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.1_top_k_2_temp_1.0_07-29-22-45.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.9_top_k_10_temp_0.1_07-29-19-32.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.9_top_k_10_temp_0.1_07-29-22-44.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.9_top_k_10_temp_0.5_07-29-19-34.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.9_top_k_10_temp_0.5_07-29-22-44.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.9_top_k_10_temp_1.0_07-29-19-37.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.9_top_k_10_temp_1.0_07-29-22-45.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.9_top_k_2_temp_0.1_07-29-19-30.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.9_top_k_2_temp_0.1_07-29-22-43.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.9_top_k_2_temp_0.5_07-29-19-32.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.9_top_k_2_temp_0.5_07-29-22-44.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.9_top_k_2_temp_1.0_07-29-19-35.json",
"test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.9_top_k_2_temp_1.0_07-29-22-45.json",
"test_queries_results_gatekeeper_True_DocRetreiver.coarse_top_p_0.1_top_k_10_temp_0.1_07-29-19-30.json",
"test_queries_results_gatekeeper_True_DocRetreiver.coarse_top_p_0.1_top_k_10_temp_0.5_07-29-19-33.json",
"test_queries_results_gatekeeper_True_DocRetreiver.coarse_top_p_0.1_top_k_10_temp_1.0_07-29-19-36.json",
"test_queries_results_gatekeeper_True_DocRetreiver.coarse_top_p_0.1_top_k_2_temp_0.1_07-29-19-25.json",
"test_queries_results_gatekeeper_True_DocRetreiver.coarse_top_p_0.1_top_k_2_temp_0.5_07-29-19-31.json",
"test_queries_results_gatekeeper_True_DocRetreiver.coarse_top_p_0.1_top_k_2_temp_1.0_07-29-19-34.json",
"test_queries_results_gatekeeper_True_DocRetreiver.coarse_top_p_0.9_top_k_10_temp_0.1_07-29-19-31.json",
"test_queries_results_gatekeeper_True_DocRetreiver.coarse_top_p_0.9_top_k_10_temp_0.5_07-29-19-34.json",
"test_queries_results_gatekeeper_True_DocRetreiver.coarse_top_p_0.9_top_k_10_temp_1.0_07-29-19-36.json",
"test_queries_results_gatekeeper_True_DocRetreiver.coarse_top_p_0.9_top_k_2_temp_0.1_07-29-19-28.json",
"test_queries_results_gatekeeper_True_DocRetreiver.coarse_top_p_0.9_top_k_2_temp_0.5_07-29-19-32.json",
"test_queries_results_gatekeeper_True_DocRetreiver.coarse_top_p_0.9_top_k_2_temp_1.0_07-29-19-35.json",
"test_queries_results_gatekeeper_True_DocRetreiver.reranker_top_p_0.1_top_k_10_temp_0.1_07-29-19-30.json",
"test_queries_results_gatekeeper_True_DocRetreiver.reranker_top_p_0.1_top_k_10_temp_0.5_07-29-19-33.json",
"test_queries_results_gatekeeper_True_DocRetreiver.reranker_top_p_0.1_top_k_10_temp_1.0_07-29-19-36.json",
"test_queries_results_gatekeeper_True_DocRetreiver.reranker_top_p_0.1_top_k_2_temp_0.1_07-29-19-26.json",
"test_queries_results_gatekeeper_True_DocRetreiver.reranker_top_p_0.1_top_k_2_temp_0.5_07-29-19-32.json",
"test_queries_results_gatekeeper_True_DocRetreiver.reranker_top_p_0.1_top_k_2_temp_1.0_07-29-19-34.json",
"test_queries_results_gatekeeper_True_DocRetreiver.reranker_top_p_0.9_top_k_10_temp_0.1_07-29-19-31.json",
"test_queries_results_gatekeeper_True_DocRetreiver.reranker_top_p_0.9_top_k_10_temp_0.5_07-29-19-34.json",
"test_queries_results_gatekeeper_True_DocRetreiver.reranker_top_p_0.9_top_k_10_temp_1.0_07-29-19-36.json",
"test_queries_results_gatekeeper_True_DocRetreiver.reranker_top_p_0.9_top_k_2_temp_0.1_07-29-19-29.json",
"test_queries_results_gatekeeper_True_DocRetreiver.reranker_top_p_0.9_top_k_2_temp_0.5_07-29-19-32.json",
"test_queries_results_gatekeeper_True_DocRetreiver.reranker_top_p_0.9_top_k_2_temp_1.0_07-29-19-35.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.1_top_k_10_temp_0.1_07-29-19-30.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.1_top_k_10_temp_0.1_07-29-22-43.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.1_top_k_10_temp_0.5_07-29-19-33.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.1_top_k_10_temp_0.5_07-29-22-44.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.1_top_k_10_temp_1.0_07-29-19-37.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.1_top_k_10_temp_1.0_07-29-22-45.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.1_top_k_2_temp_0.1_07-29-19-27.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.1_top_k_2_temp_0.1_07-29-22-42.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.1_top_k_2_temp_0.5_07-29-19-32.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.1_top_k_2_temp_0.5_07-29-22-44.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.1_top_k_2_temp_1.0_07-29-19-35.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.1_top_k_2_temp_1.0_07-29-22-45.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.9_top_k_10_temp_0.1_07-29-19-31.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.9_top_k_10_temp_0.1_07-29-22-44.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.9_top_k_10_temp_0.5_07-29-19-35.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.9_top_k_10_temp_0.5_07-29-22-44.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.9_top_k_10_temp_1.0_07-29-19-37.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.9_top_k_10_temp_1.0_07-29-22-45.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.9_top_k_2_temp_0.1_07-29-19-30.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.9_top_k_2_temp_0.1_07-29-22-42.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.9_top_k_2_temp_0.5_07-29-19-33.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.9_top_k_2_temp_0.5_07-29-22-44.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.9_top_k_2_temp_1.0_07-29-19-35.json",
"test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.9_top_k_2_temp_1.0_07-29-22-45.json"
]

# Function to parse a filename into a tuple of parameters
def parse_filename(filename):
    parts = filename.split('_')
    use_gatekeeper = 'True' in filename
    retriever = filename.split('DocRetreiver.')[1].split('_')[0]
    top_p = float(filename.split('top_p_')[1].split('_')[0])
    top_k = int(filename.split('top_k_')[1].split('_')[0])
    temperature = float(filename.split('temp_')[1].split('_')[0])
    timestamp = filename.split('_')[-1].split('.')[0]
    return (temperature, top_k, top_p, retriever, use_gatekeeper, timestamp, filename)

# Extract tuples from generated filenames
file_tuples = [parse_filename(f) for f in generated_files]

# Dictionary to store files by their key (excluding timestamp and filename)
file_dict = defaultdict(list)
for file_tuple in file_tuples:
    key = file_tuple[:-2]  # Exclude timestamp and filename for the key
    file_dict[key].append(file_tuple)

# Find and log duplicates
duplicates = []
for key, files in file_dict.items():
    if len(files) > 1:
        # Sort files by timestamp
        sorted_files = sorted(files, key=lambda x: x[-2])
        # Exclude the newest file
        duplicates.extend(sorted_files[:-1])

# Print duplicates
print("Duplicates (excluding the newest file):")
for dup in duplicates:
    print(dup[-1])  # Print the filename

# Write duplicates to a file
with open("duplicates.txt", "w") as f:
    for dup in duplicates:
        f.write(dup[-1] + "\n")

# Example to delete duplicates
# for dup in duplicates:
#     os.remove(dup[-1])
