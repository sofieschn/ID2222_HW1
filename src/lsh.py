import numpy as np
from collections import defaultdict

class LSH:
    def __init__(self, num_bands, rows_per_band, similarity_threshold):
        self.num_bands = num_bands  # Number of bands
        self.rows_per_band = rows_per_band  # Rows per band
        self.similarity_threshold = similarity_threshold  # Similarity threshold for candidate pairs

    def hash_band(self, band):
        """Hashes a single band (list of integers) into a hash value."""
        return hash(tuple(band))

    def find_candidate_pairs(self, minhash_signatures):
        """
        Given a collection of minhash signatures, find candidate pairs using LSH.
        Args:
            minhash_signatures: List of minhash signatures (each signature is a list of integers)
        Returns:
            candidate_pairs: A set of tuples representing candidate pairs of similar documents
        """
        num_docs = len(minhash_signatures)
        if num_docs == 0:
            return set()

        # Ensure the signatures are divided evenly into bands
        signature_length = len(minhash_signatures[0])
        assert signature_length == self.num_bands * self.rows_per_band, "Inconsistent signature length."

        candidate_pairs = set()
        band_hashes = defaultdict(list)  # Maps band hashes to document indices

        # For each band, hash the rows in that band and group documents by hash value
        for band_idx in range(self.num_bands):
            band_hashes.clear()  # Clear band hashes for current band
            for doc_idx, signature in enumerate(minhash_signatures):
                start_idx = band_idx * self.rows_per_band
                end_idx = (band_idx + 1) * self.rows_per_band
                band = signature[start_idx:end_idx]
                band_hash = self.hash_band(band)
                band_hashes[band_hash].append(doc_idx)

            # For each hash bucket, all documents in the bucket are candidates
            for docs in band_hashes.values():
                if len(docs) > 1:  # Only consider pairs if there's more than one doc in the bucket
                    for i in range(len(docs)):
                        for j in range(i + 1, len(docs)):
                            candidate_pairs.add((docs[i], docs[j]))

        return candidate_pairs

    def filter_candidates(self, candidate_pairs, minhash_signatures, similarity_func):
        """
        Filters candidate pairs based on actual similarity.
        Args:
            candidate_pairs: Set of candidate pairs identified by LSH
            minhash_signatures: List of minhash signatures
            similarity_func: Function to compute similarity (e.g., CompareSignatures.signature_similarity)
        Returns:
            filtered_pairs: A list of tuples (doc1, doc2, similarity) where similarity >= threshold
        """
        filtered_pairs = []
        for doc1, doc2 in candidate_pairs:
            similarity = similarity_func(minhash_signatures[doc1], minhash_signatures[doc2])
            if similarity >= self.similarity_threshold:
                filtered_pairs.append((doc1, doc2, similarity))
        return filtered_pairs
