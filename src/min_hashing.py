import numpy as np
import hashlib

class MinHashing: 
    def __init__(self, num_hashes):
        self.num_hashes = num_hashes  # Specifies the length of the minhash signature
        self.max_shingle_id = 2**32-1  # Just a large number
        self.rng = np.random.default_rng()  # Use default random number generator
        self.hash_functions = self.generate_hash_functions()  # A list of tuples representing the hash functions

    def generate_hash_functions(self):
        """
        Generates a list of hash functions using random coefficients a and b.
        """
        a = self.rng.integers(1, self.max_shingle_id, self.num_hashes, dtype=np.int64)
        b = self.rng.integers(0, self.max_shingle_id, self.num_hashes, dtype=np.int64)
        return np.vstack((a, b))

    def minhash_signature(self, shingle_set): 
        """
        Creates a minhash signature for a given set of shingles.
        """
        shingles = np.array(list(shingle_set))
        hash_matrix = (self.hash_functions[0] * shingles[:, None] + self.hash_functions[1]) % self.max_shingle_id
        signature = hash_matrix.min(axis=0)
        return signature.tolist()
