import hashlib


""""---------Step 1: Shingling: Convert documents to sets----------"""

class Shingling: 
    def _init_(self, k) :
        self.k=k # k is the length of the shingle

    # function creates shingles of the data in the document
    def create_shingles(self, document) :
        shingles = set()
        # loop document extracting shingles of length k
        for i in range(len(document) - self.k + 1) : 
            shingle = document[i:i + self.k] 
            hashed_shingle = self.hash_shingle(shingle) # call hash function to hash each shingle
            shingles.add(hashed_shingle) 
            return shingles
        

    # each shingle needs to be hashed for comparison later
    # .encode('utf-8') converts shingle to value MD5 can read
    # MD5 is from the hashlib lib, converts shingle to hash value
    # hexdigest() converts the string to int
    def hash_shingle(self, shingle):
        hashed_shingle = int(hashlib.md5(shingle.encode('utf.8')).hexdigest(),16) 
        return hashed_shingle

