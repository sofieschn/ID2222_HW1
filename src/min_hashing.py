import numpy as np
import random


""""---------Step 2: Minhashing: Convert large sets to
            short signatures while preserving similarity----------"""

class MinHashing: 
    def __init__(self, num_hashes):
        self.num_hashes = num_hashes  # Specifies the length of the minhash signature (number of hash functions).
        self.max_shingle_id = 2**32 - 1  # Just a large number for hashing
        self.hash_functions = self.generate_hash_functions()  # A list of tuples representing the hash functions

    def generate_hash_functions(self):
        # Use np.random.default_rng to support larger ranges
        rng = np.random.default_rng()
        
        a = rng.integers(1, self.max_shingle_id, self.num_hashes, dtype='uint64')
        b = rng.integers(0, self.max_shingle_id, self.num_hashes, dtype='uint64')
        return np.vstack((a, b))  # Stack the hash coefficients vertically

    def minhash_signature(self, shingle_set): 
        # Step 1: Convert the shingle set to a NumPy array
        shingles = np.array(list(shingle_set))  
        
        # Step 2: Prepare to calculate hashes for each shingle with each hash function
        hash_matrix = (self.hash_functions[0] * shingles[:, None] + self.hash_functions[1]) % self.max_shingle_id
        
        # Step 3: For each hash function (each column in the hash matrix), find the minimum hash value across all shingles.
        signature = hash_matrix.min(axis=0)
        
        # Step 4: Convert the signature to a regular Python list and return
        return signature.tolist()