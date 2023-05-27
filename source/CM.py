import networkx as nx
import json
import numpy as np
import pathlib
import os

class SpreadingActivationModel:
    def __init__(self, parameter):
        # define member variable
        self.parameter = parameter
    
        self.__lexiconNetwork = nx.read_gml(f'{os.path.expanduser("~")}/Project/Resource/SimilarityNetwork-k10.gml')
        nx.set_node_attributes(self.__lexiconNetwork, 0.0, "resevoir")

    def getLexiconNetwork(self):
        return self.__lexiconNetwork

    def randomWalk(self, targetWord):
        # Next target node choice following probablity by cosine similarity  between current target node and each neighborhood node
        # 1. Probablity of choiced node make a calculation follwoing weight between nodes
        iterNeighbors = list(self.__lexiconNetwork.neighbors(targetWord))
        neighbors = iterNeighbors
        
        weights = np.array([self.__lexiconNetwork[node][targetWord]["weight"] for node in iterNeighbors])
        probability = weights / np.sum(weights)

        # 2. Choice next target nord by probability calulated at step 1.
        nextTargetNord = np.random.choice(neighbors, p=probability)

        return nextTargetNord
    
        
    def activation(self, initTargetWord):

        # Whether initial target word exist in lexicon network
        if initTargetWord not in self.__lexiconNetwork.nodes:
            print(f"'{initTargetWord}' not in lexicon network...")
            return

        r = self.parameter["r"]
        targetWord = initTargetWord

        for i in range(self.parameter["T"]):

            # 1. Next target node receive "inflow" value caluclate by current node`s outflow and next node's reservoir.
            if i == 0:
                inflow = 100 + self.__lexiconNetwork.nodes[targetWord]["resevoir"]
            else:
                inflow = outflow + self.__lexiconNetwork.nodes[targetWord]["resevoir"]

            # 2. "resevoir" is representing activation value in each node
            resevoir = r * inflow

            # 3. Renew resvoir of current target node
            self.__lexiconNetwork.nodes[targetWord]["resevoir"] = resevoir

            # 4. "outflow" is amount of following out to next target nord
            outflow = (1 - r) * inflow
            #print(f"resevoir:{resevoir} outflow:{outflow} inflow:{inflow}")

            # 5. Next target node choice following probablity by cosine similarity  between current target node and each neighborhood node
            nextTargetWord = self.randomWalk(targetWord)
            #print(f"next target:{nextTargetWord}")

            # 1.  Move to next target node
            targetWord = nextTargetWord
        


        

