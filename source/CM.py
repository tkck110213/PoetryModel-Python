import networkx as nx
import json
import numpy as np
import pathlib
import os

class SpreadingActivationModel:
    def __init__(self, parameter):
        # define member variable
        self.parameter = parameter

        print("loading lexicon network...")
        self._lexiconNetwork = nx.read_gml(f'{os.path.expanduser("~")}/Project/Resource/SimilarityNetwork-k10.gml', label="id")
        nx.set_node_attributes(self._lexiconNetwork, 0.0, "resevoir")
        print("Comlete loading lexicon network!")

        self._dicLabel2Index = {str(self._lexiconNetwork.nodes[i]["label"]):i for i in range(len(self._lexiconNetwork.nodes))}
        

    def getLexiconNetwork(self):
        return self._lexiconNetwork

    def randomWalk(self, targetWordIndex):
        # Next target node choice following probablity by cosine similarity  between current target node and each neighborhood node
        # 1. Probablity of choiced node make a calculation follwoing weight between nodes
        iterNeighbors = list(self._lexiconNetwork.neighbors(targetWordIndex))
        neighbors = iterNeighbors

        weights = np.array([self._lexiconNetwork[nodeIndex][targetWordIndex]["weight"] for nodeIndex in iterNeighbors])
        probability = weights / np.sum(weights)

        # 2. Choice next target nord by probability calulated at step 1.
        nextTargetNordIndex = np.random.choice(neighbors, p=probability)

        return nextTargetNordIndex
    
        
    def activation(self, initTargetWord):

        # Whether initial target word exist in lexicon network
        if initTargetWord not in self._dicLabel2Index.keys():
            print(f"'{initTargetWord}' not in lexicon network...")
            return

        r = self.parameter["r"]
        targetWordIndex = self._dicLabel2Index[initTargetWord]

        for i in range(self.parameter["T"]):

            # 1. Next target node receive "inflow" value caluclate by current node`s outflow and next node's reservoir.
            if i == 0:
                inflow = 100 + self._lexiconNetwork.nodes[targetWordIndex]["resevoir"]
            else:
                inflow = outflow + self._lexiconNetwork.nodes[targetWordIndex]["resevoir"]

            # 2. "resevoir" is representing activation value in each node
            resevoir = r * inflow

            # 3. Renew resvoir of current target node
            self._lexiconNetwork.nodes[targetWordIndex]["resevoir"] = resevoir

            # 4. "outflow" is amount of following out to next target nord
            outflow = (1 - r) * inflow
            #print(f"resevoir:{resevoir} outflow:{outflow} inflow:{inflow}")

            # 5. Next target node choice following probablity by cosine similarity  between current target node and each neighborhood node
            nextTargetWordIndex = self.randomWalk(targetWordIndex)
            #print(f"next target:{nextTargetWord}")

            # 1.  Move to next target node
            targetWordIndex = nextTargetWordIndex
        


        

