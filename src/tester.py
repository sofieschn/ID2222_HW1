import os
import json
import time
from shingling import Shingling
from compare_sets import CompareSets

# Set the absolute path to the Data folder
data_folder = "/Users/sofieschnitzer/Desktop/KTH_HT24_filer/ID2222/upg/DataMining_HW1/src/Data"

def load_articles(data_folder):
    """Loads article texts from JSON files in the specified folder."""
    articles = []
    # Iterate through each JSON file in the Data directory
    for filename in sorted(os.listdir(data_folder)):
        if filename.endswith(".json"):
            file_path = os.path.join(data_folder, filename)
            try:
                # Open and load the JSON file
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    # Append the article's "text" field to the list
                    articles.append(data["text"])  # Adjust if the JSON structure differs
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    
    return articles

def run_scalability_test(corpus, k, similarity_threshold):
    # Step 1: Initialize Shingling
    shingler = Shingling(k)
    
    # Step 2: Create shingles for each document in the corpus
    shingle_sets = []
    for doc in corpus:
        shingle_set = shingler.create_shingles(doc)
        shingle_sets.append(shingle_set)

    # Step 3: Measure time and compare Jaccard similarities for each document pair
    start_time = time.time()
    similar_pairs = []  # To store document pairs that meet the similarity threshold
    
    # Compare each document pair
    for i in range(len(corpus)):
        for j in range(i + 1, len(corpus)):  # Only compare each pair once
            jaccard_similarity = CompareSets.jaccard_similarity(shingle_sets[i], shingle_sets[j])
            if jaccard_similarity >= similarity_threshold:
                similar_pairs.append((i, j, jaccard_similarity))
    
    # Step 4: Measure end time
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Step 5: Output the results
    print(f"Execution Time: {elapsed_time:.4f} seconds")
    print(f"Similar Document Pairs (Threshold {similarity_threshold}):")
    for (doc1, doc2, sim) in similar_pairs:
        print(f"Document {doc1 + 1} and Document {doc2 + 1} - Jaccard Similarity: {sim:.4f}")

# Load the articles from the Data folder
corpus = load_articles(data_folder)

# Only proceed if articles were loaded successfully
if corpus:
    # Run the scalability test with chosen parameters
    k = 5  # Shingle length
    similarity_threshold = 0.8  # Similarity threshold for identifying similar documents

    run_scalability_test(corpus, k, similarity_threshold)
else:
    print("No articles were loaded. Please check the Data folder path and contents.")
