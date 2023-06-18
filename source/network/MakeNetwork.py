import networkx as nx
from gensim.models import KeyedVectors
import re
from tqdm import tqdm
import sys
import os

class SimilarNetwork:
    def __init__(self):
        path = f'{os.path.expanduser("~")}/Project/Resource/lexicon_network_s0.400000.graphml'
        print(f"model path:{path}")
        print("Word2Vec loading...")
        self.model = KeyedVectors.load_word2vec_format(path)
        print("Complete Word2Vec loading")

        self.wordlist = self.model.index_to_key
        self.similarityNetwork = nx.Graph()
        
    def makeSimilarNetwork(self, k):
        for word in tqdm(self.wordlist):
            similarWords = self.model.most_similar(positive=[word], topn=k)
            self.similarityNetwork.add_weighted_edges_from([(re.sub("##", "", word), re.sub("##", "", similar[0]), similar[1]) for similar in similarWords])

        nx.write_gml(self.similarityNetwork, f'{os.path.expanduser("~")}/Project/Resource/SimilarityNetwork-k{k}.gml')
        


def main(k):
    sn = SimilarNetwork()
    sn.makeSimilarNetwork(k)

main(int(sys.argv[1]))

