import networkx as nx
from gensim.models import KeyedVectors
import re
from tqdm import tqdm
import sys


class SimilarNetwork:
    def __init__(self):
        print("Word2Vec loading...")
        self.model = KeyedVectors.load_word2vec_format("~/Project/Resource/jawiki.all_vectors.200d.txt")
        self.wordlist = self.model.index_to_key

        self.similarityNetwork = nx.Graph()
        print("Complete Word2Vec loading")
    def makeSimilarNetwork(self, limit_similarity=0.5):
        self.similarityNetwork.add_nodes_from(self.wordlist)

        #自分以外のノード全てと類似度を求め，limit_simirality以上ならエッジを作る
        for i, word1 in enumerate(tqdm(self.wordlist)):
            for word2 in self.wordlist[i + 1:]:
                if word1 in self.wordlist and word2 in self.wordlist:
                    #ワード間の類似度を算出
                    similarity = self.model.similarity(word1, word2)
                    if limit_similarity < similarity:
                        word1 = re.sub("##", "", word1)
                        word2 = re.sub("##", "", word2)
                        self.similarityNetwork.add_edges_from([(word1, word2, {"similarity":str(similarity)})])

        nx.write_gml(self.similarityNetwork, f"SimilarityNetwork-s{limit_similarity}.gml")
        


def main(similar):
    sn = SimilarNetwork()
    sn.makeSimilarNetwork(limit_similarity=similar)

main(float(sys.argv[1]))
