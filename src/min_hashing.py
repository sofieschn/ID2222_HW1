import numpy as np
import random


""""---------Step 2: Minhashing: Convert large sets to
            short signatures while preserving similarity----------"""

class MinHashing: 
    def __init__(self, num_hashes):
        self.num_hashes = num_hashes # Specifies the length of the minhash signature (the number of hash functions to use).
        self.max_shingle_id = 2**32-1 #just a large nr (could be 4834858345 as well)
        self.hash_functions = self.generate_hash_functions() #A list of tuples representing the hash functions

    

    def generate_hash_functions(self):
        # creates two arrays for a and b, each as long as "num_hashes"
        # 
        a = np.random.randint(1, self.max_shingle_id, self.num_hashes)
        b = np.random.randint(0, self.max_shingle_id, self.num_hashes)
        return np.vstack((a,b)) # stacks the two arrays vertically next to eachother and returns this stack
    

    def minhash_signature(self, shingle_set): 
        # Step 1: Convert the shingle set to a NumPy array
        shingles = np.array(list(shingle_set))  
        
        # Step 2: Prepare to calculate hashes for each shingle with each hash function
        # Hash function: (a * shingle + b) % max_shingle_id for each hash function
        # Apply all hash functions to all shingles at once, storing the results in a hash matrix.
        hash_matrix = (self.hash_functions[0] * shingles[:, None] + self.hash_functions[1]) % self.max_shingle_id
        
        # Step 3: For each hash function (each column in the hash matrix), find the minimum hash value across all shingles.
        # Each column represents a different hash function; we take the min across each column
        signature = hash_matrix.min(axis=0)
        
        # Step 4: Convert the signature to a reg python list and return
        return signature.tolist()






