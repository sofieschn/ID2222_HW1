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

def explore_similarities(corpus, k):
    """Calculate and display similarity scores for all document pairs."""
    # Step 1: Initialize Shingling
    shingler = Shingling(k)
    
    # Step 2: Create shingles for each document in the corpus
    shingle_sets = []
    for doc in corpus:
        shingle_set = shingler.create_shingles(doc)
        shingle_sets.append(shingle_set)

    # Step 3: Measure time and compare Jaccard similarities for each document pair
    start_time = time.time()
    similarity_scores = []  # Store all document pair similarities
    
    # Compare each document pair
    for i in range(len(corpus)):
        for j in range(i + 1, len(corpus)):  # Only compare each pair once
            jaccard_similarity = CompareSets.jaccard_similarity(shingle_sets[i], shingle_sets[j])
            similarity_scores.append((i, j, jaccard_similarity))
    
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Step 4: Output the results
    print(f"Execution Time: {elapsed_time:.4f} seconds")
    print("Similarity Scores for All Document Pairs:")
    for (doc1, doc2, sim) in similarity_scores:
        print(f"Document {doc1 + 1} and Document {doc2 + 1} - Jaccard Similarity: {sim:.4f}")

# Load the articles from the Data folder
corpus = load_articles(data_folder)

# Only proceed if articles were loaded successfully
if corpus:
    # Run the similarity exploration with chosen parameters
    k = 5  # Shingle length
    explore_similarities(corpus, k)
else:
    print("No articles were loaded. Please check the Data folder path and contents.")
