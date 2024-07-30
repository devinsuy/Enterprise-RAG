import itertools

# Configuration options
temperatures = [0.1, 0.5, 1.0]
top_ks = [2, 10]
top_ps = [0.1, 0.9]
retrievers = ["coarse", "reranker", "self_query_chain"]
use_gatekeeper_queries = [True, False]

# Generate all permutations of the configurations
all_permutations = list(itertools.product(temperatures, top_ks, top_ps, retrievers, use_gatekeeper_queries))


# List of files generated from your output
generated_files = [
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
    "test_queries_results_gateke# Extract the relevant parteper_False_DocRetreiver.reranker_top_p_0.1_top_k_2_temp_0.5_07-29-19-31.json",
    "test_queries_results_gatekeeper_False_DocRetreiver.reranker_top_p_0.1_top_k_2_temp_1.0_07-29-19-34.json",
    "test_queries_results_gatekeeper_False_DocRetreiver.reranker_top_p_0.9_top_k_10_temp_0.1_07-29-19-31.json",
    "test_queries_results_gatekeeper_False_DocRetreiver.reranker_top_p_0.9_top_k_10_temp_0.5_07-29-19-34.json",
    "test_queries_results_gatekeeper_False_DocRetreiver.reranker_top_p_0.9_top_k_10_temp_1.0_07-29-19-37.json",
    "test_queries_results_gatekeeper_False_DocRetreiver.reranker_top_p_0.9_top_k_2_temp_0.1_07-29-19-29.json",
    "test_queries_results_gatekeeper_False_DocRetreiver.reranker_top_p_0.9_top_k_2_temp_0.5_07-29-19-32.json",
    "test_queries_results_gatekeeper_False_DocRetreiver.reranker_top_p_0.9_top_k_2_temp_1.0_07-29-19-36.json",
    "test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.1_top_k_10_temp_0.1_07-29-19-31.json",
    "test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.1_top_k_10_temp_0.5_07-29-19-33.json",
    "test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.1_top_k_10_temp_1.0_07-29-19-36.json",
    "test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.1_top_k_2_temp_0.1_07-29-19-28.json",
    "test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.1_top_k_2_temp_0.5_07-29-19-32.json",
    "test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.1_top_k_2_temp_1.0_07-29-19-35.json",
    "test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.9_top_k_10_temp_0.1_07-29-19-32.json",
    "test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.9_top_k_10_temp_0.5_07-29-19-34.json",
    "test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.9_top_k_10_temp_1.0_07-29-19-37.json",
    "test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.9_top_k_2_temp_0.1_07-29-19-30.json",
    "test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.9_top_k_2_temp_0.5_07-29-19-32.json",
    "test_queries_results_gatekeeper_False_DocRetreiver.self_query_chain_top_p_0.9_top_k_2_temp_1.0_07-29-19-35.json",
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
    "test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.1_top_k_10_temp_0.5_07-29-19-33.json",
    "test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.1_top_k_10_temp_1.0_07-29-19-37.json",
    "test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.1_top_k_2_temp_0.1_07-29-19-27.json",
    "test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.1_top_k_2_temp_0.5_07-29-19-32.json",
    "test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.1_top_k_2_temp_1.0_07-29-19-35.json",
    "test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.9_top_k_10_temp_0.1_07-29-19-31.json",
    "test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.9_top_k_10_temp_0.5_07-29-19-35.json",
    "test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.9_top_k_10_temp_1.0_07-29-19-37.json",
    "test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.9_top_k_2_temp_0.1_07-29-19-30.json",
    "test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.9_top_k_2_temp_0.5_07-29-19-33.json",
    "test_queries_results_gatekeeper_True_DocRetreiver.self_query_chain_top_p_0.9_top_k_2_temp_1.0_07-29-19-35.json",
]

# Function to parse a filename into a tuple of parameters
def parse_filename(filename):
    use_gatekeeper = 'True' in filename
    retriever = filename.split('DocRetreiver.')[1].split('_')[0]
    top_p = float(filename.split('top_p_')[1].split('_')[0])
    top_k = int(filename.split('top_k_')[1].split('_')[0])
    temperature = float(filename.split('temp_')[1].split('_')[0])
    return (temperature, top_k, top_p, retriever, use_gatekeeper)

# Extract tuples from generated filenames
generated_tuples = [parse_filename(f) for f in generated_files]

# Find missing permutations
missing_permutations = [perm for perm in all_permutations if perm not in generated_tuples]

# Print missing permutations
for missing in missing_permutations:
    print("Missing permutation:", missing)