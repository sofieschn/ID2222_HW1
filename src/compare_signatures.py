
""""---------Step 3: Comapring signatures: The goal is to compare 
two minhash signatures by checking how many elements they have in common, 
which serves as an approximate measure of the similarity between the 
original documents.----------"""


class CompareSignatures: 
    @staticmethod
    def signature_similarity(signature1, signature2):
        # takes to minhash signatures and checks the similarity between the two
        # first checks that the length of the 2 are the same 
        if len(signature1) != len(signature2):
            raise ValueError("Same length signatures only")
        

        # iterates each position in signatures and checks if the elements at each position 
        # are the same in both signatures. 
        # each time a match is found, 1 is added to the count (match_count holds number of matches)
        match_count = sum(1 for i in range(len(signature1)) if signature1[i] == signature2[i])

        # the returned value will be the number of matches / the length of the signature(s)
        # this will give a result such as 4 / 6 = 0.6667 (if signature length is 6 and matches are 4, very similar in this ex)
        return match_count/len(signature1)
        



