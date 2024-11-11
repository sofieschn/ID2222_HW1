import numpy as np
from collections import defaultdict
from compare_signatures import CompareSignatures

class LSH:
    def __init__(self, num_bands, rows_per_band):
        """
        Initializes the LSH class with the given number of bands and rows per band.
        
        :param num_bands: Number of bands.
        :param rows_per_band: Number of rows per band (must multiply to the length of the minhash signatures).
        """
        self.num_bands = num_bands
        self.rows_per_band = rows_per_band
        self.buckets = [defaultdict(list) for _ in range(num_bands)]

    def hash_band(self, band):
        """Hashes a band to a bucket."""
        return hash(tuple(band))

    def fit(self, signatures):
        """
        Fits the LSH model by placing document signatures into buckets.
        
        :param signatures: List of minhash signatures.
        """
        for doc_id, signature in enumerate(signatures):
            for band_index in range(self.num_bands):
                start = band_index * self.rows_per_band
                end = start + self.rows_per_band
                band = signature[start:end]
                bucket = self.hash_band(band)
                self.buckets[band_index][bucket].append(doc_id)

    def find_candidates(self):
        """
        Finds candidate pairs based on the LSH buckets.
        
        :return: A set of candidate pairs (doc1, doc2).
        """
        candidate_pairs = set()
        for band_index in range(self.num_bands):
            for bucket, doc_ids in self.buckets[band_index].items():
                if len(doc_ids) > 1:
                    for i in range(len(doc_ids)):
                        for j in range(i + 1, len(doc_ids)):
                            candidate_pairs.add((doc_ids[i], doc_ids[j]))
        return candidate_pairs

    def filter_candidates(self, signatures, threshold):
        """
        Filters candidate pairs to only those above the similarity threshold.
        
        :param signatures: List of minhash signatures.
        :param threshold: Similarity threshold.
        :return: List of candidate pairs with similarity above the threshold.
        """
        candidate_pairs = self.find_candidates()
        confirmed_pairs = []

        for doc1, doc2 in candidate_pairs:
            similarity = CompareSignatures.signature_similarity(signatures[doc1], signatures[doc2])
            if similarity >= threshold:
                confirmed_pairs.append((doc1, doc2, similarity))

        return confirmed_pairs
