import os
import json
import time
from shingling import Shingling
from compare_sets import CompareSets
from lsh import LSH
from min_hashing import MinHashing

def load_articles():
    """Loads article texts from JSON files in the 'Data' folder relative to this script's location."""
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Define the Data folder relative to the script
    data_folder = os.path.join(script_dir, "Data")

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

def explore_similarities(corpus, k, num_hashes=125, num_bands=25, threshold=0.6):
    """Calculate and display similarity scores using LSH for all document pairs."""
    
    # Step 1: Print loaded documents
    print("\nLoaded Documents:")
    for idx, doc in enumerate(corpus):
        print(f"Document {idx + 1}: {doc[:200]}...")  # Print the first 200 characters for brevity

    # Step 2: Initialize Shingling
    shingler = Shingling(k)
    
    # Step 3: Create shingles for each document in the corpus
    shingle_sets = [shingler.create_shingles(doc) for doc in corpus]

    # Step 4: Minhashing
    minhasher = MinHashing(num_hashes)
    start_time_minhash = time.time()
    signatures = [minhasher.minhash_signature(shingle_set) for shingle_set in shingle_sets]
    end_time_minhash = time.time()

    # Step 5: LSH
    rows_per_band = num_hashes // num_bands
    lsh = LSH(num_bands, rows_per_band)
    start_time_lsh = time.time()
    lsh.fit(signatures)
    candidates = lsh.filter_candidates(signatures, threshold)
    end_time_lsh = time.time()

    # Output timing results
    print(f"\nMinHashing Execution Time: {end_time_minhash - start_time_minhash:.4f} seconds")
    print(f"LSH Execution Time: {end_time_lsh - start_time_lsh:.4f} seconds")
    print(f"Total Execution Time: {end_time_lsh - start_time_minhash:.4f} seconds")

    # Step 6: Output LSH candidate pairs
    print(f"\nLSH Candidate Pairs with Similarity >= {threshold}:")
    if candidates:
        for doc1, doc2, sim in candidates:
            print(f"Document {doc1 + 1} and Document {doc2 + 1} - Similarity: {sim:.4f}")
    else:
        print("No candidate pairs found.")

    # Step 7: True Jaccard Similarities
    print("\nCalculating True Jaccard Similarities for All Pairs...")
    for i in range(len(corpus)):
        for j in range(i + 1, len(corpus)):
            jaccard_sim = CompareSets.jaccard_similarity(shingle_sets[i], shingle_sets[j])
            print(f"Document {i + 1} and Document {j + 1} - True Jaccard Similarity: {jaccard_sim:.4f}")

# Load the articles from the Data folder
corpus = load_articles()

# Only proceed if articles were loaded successfully
if corpus:
    # Run the similarity exploration with chosen parameters
    k = 5  # Shingle length
    num_hashes = 125  # Number of hash functions for MinHashing
    num_bands = 25  # Number of bands for LSH
    threshold = 0.6  # Similarity threshold

    explore_similarities(corpus, k, num_hashes=num_hashes, num_bands=num_bands, threshold=threshold)
else:
    print("No articles were loaded. Please check the Data folder path and contents.")