

""""---------Step 4: Comapring sets: The Jaccard similarity measures how 
similar two sets are based on the ratio of their intersection (common elements) 
to their union (all unique elements). gives us the “true” similarity between the 
original documents, which we can later compare with the approximate similarity 
given by the minhash signatures..----------"""

# calculates the jaccard sim between two sets of hashed shingles

class CompareSets:
    @staticmethod 
    def jaccard_similarity(set1, set2):
        #step1 find the intersection of the 2 sets
        intersection = len(set1.intersection(set2))

        #step2 find the unsion of the 2 sets 
        union = len(set1.union(set2))

        # step 3 calculate and return the jaccard similarity
        jaccard_sim = intersection / union if union != 0 else 0

        return jaccard_sim
    

    
