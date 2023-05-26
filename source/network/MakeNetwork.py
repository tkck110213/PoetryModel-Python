import networkx as nx
from gensim.models import KeyedVectors
import re
from tqdm import tqdm
import sys


class SimilarNetwork:
    def __init__(self):
        print("Word2Vec loading...")
        self.model = KeyedVectors.load_word2vec_format("~/Project/Resource/jawiki.all_vectors.200d.txt")
        print("Complete Word2Vec loading")

        self.wordlist = self.model.index_to_key
        self.similarityNetwork = nx.Graph()
        
    def makeSimilarNetwork(self, k):
        for word in tqdm(self.wordlist):
            similarWords = self.model.most_similar(positive=[word], topn=k)
            self.similarityNetwork.add_weighted_edges_from([(re.sub("##", "", word), re.sub("##", "", similar[0]), similar[1]) for similar in similarWords])

        nx.write_gml(self.similarityNetwork, f"~/Project/Resource/SimilarityNetwork-k{k}.gml")
        


def main(k):
    sn = SimilarNetwork()
    sn.makeSimilarNetwork(k)

main(int(sys.argv[1]))

