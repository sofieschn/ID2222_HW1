import os
import json
import time
from shingling import Shingling
from compare_sets import CompareSets
from min_hashing import MinHashing
from compare_signatures import CompareSignatures
from lsh import LSH

# Locate the Data folder dynamically based on the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the script
data_folder = os.path.join(script_dir, "Data")  # Adjust if Data is in a subdirectory

def load_articles(data_folder):
    """Loads article texts from JSON files in the specified folder."""
    articles = []
    for filename in sorted(os.listdir(data_folder)):
        if filename.endswith(".json"):
            file_path = os.path.join(data_folder, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    if isinstance(data, list) and len(data) > 0:
                        articles.append(data[0]["text"])  # Access "text" in the first dictionary in the list
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    
    return articles

def explore_similarities_with_lsh(corpus, k, num_hashes, num_bands, rows_per_band, similarity_threshold):
    """Calculate and display similarity scores for all document pairs using LSH."""
    # Step 1: Initialize Shingling and MinHashing
    shingler = Shingling(k)
    minhasher = MinHashing(num_hashes)
    lsh = LSH(num_bands, rows_per_band, similarity_threshold)
    
    # Step 2: Create shingles and MinHash signatures for each document
    shingle_sets = []
    minhash_signatures = []
    
    for doc in corpus:
        shingle_set = shingler.create_shingles(doc)
        shingle_sets.append(shingle_set)
        minhash_signature = minhasher.minhash_signature(shingle_set)
        minhash_signatures.append(minhash_signature)

    # Step 3: Use LSH to find candidate pairs
    start_time = time.time()
    candidate_pairs = lsh.find_candidate_pairs(minhash_signatures)
    
    # Step 4: Filter candidate pairs based on actual similarity
    filtered_pairs = lsh.filter_candidates(candidate_pairs, minhash_signatures, CompareSignatures.signature_similarity)
    end_time = time.time()

    elapsed_time = end_time - start_time

    # Step 5: Output the results
    print(f"Execution Time with LSH: {elapsed_time:.4f} seconds")
    print(f"Candidate Pairs (Similarity >= {similarity_threshold}):")
    for doc1, doc2, sim in filtered_pairs:
        print(f"Document {doc1 + 1} and Document {doc2 + 1}: Similarity = {sim:.4f}")

# Load the articles from the Data folder
corpus = load_articles(data_folder)

# Only proceed if articles were loaded successfully
if corpus:
    # Run the similarity exploration with chosen parameters
    k = 5  # Shingle length
    num_hashes = 100  # Number of hash functions for MinHash
    num_bands = 20  # Number of bands in LSH
    rows_per_band = 5  # Rows per band in LSH
    similarity_threshold = 0.8  # Threshold for LSH

    explore_similarities_with_lsh(corpus, k, num_hashes, num_bands, rows_per_band, similarity_threshold)
else:
    print("No articles were loaded. Please check the Data folder path and contents.")
