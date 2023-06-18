import networkx as nx
import json
import numpy as np
import pathlib
import os
import utility.util as util

class SpreadingActivationModel:
    def __init__(self, parameter):
        # define member variable
        self.parameter = parameter

        print("loading lexicon network...")
        self._lexiconNetwork = nx.read_graphml(f'{os.path.expanduser("~")}/Project/Resource/lexicon_network_s0.400000.graphml', label="id")
        nx.set_node_attributes(self._lexiconNetwork, 0.0, "reservoir")
        nx.set_node_attributes(self._lexiconNetwork, 0.0, "inflow")
        nx.set_node_attributes(self._lexiconNetwork, 0.0, "outflow")
        print("Comlete loading lexicon network!")

        self._dicLabel2Id = {str(self._lexiconNetwork.nodes[i]["label"]):i for i in range(len(self._lexiconNetwork.nodes))}
        

    def getLexiconNetwork(self):
        return self._lexiconNetwork

    def renewNeighborsInflow(self, targetWordId):
        neighbors = list(self._lexiconNetwork.neighbors(targetWordId))
        outflow = self._lexiconNetwork.nodes[targetWordId]["outflow"]

        weights = np.array([self._lexiconNetwork[neighbors[i]][targetWordId]["weight"] for i in range(len(neighbors))])
        weights = weights / np.sum(weights)

        for nodeId, w in zip(neighbors, weights):
            self._lexiconNetwork.nodes[nodeId]["inflow"] = self._lexiconNetwork.nodes[nodeId]["reservoir"] + outflow * w

        return neighbors


    def activation(self, initTargetWord):

        # Whether initial target word exist in lexicon network
        if initTargetWord not in self._dicLabel2Id.keys():
            print(f"'{initTargetWord}' not in lexicon network...")
            return

        r = self.parameter["r"]
        targetWordsId = [self._dicLabel2Id[initTargetWord]]
        nextTargetWordsId = []

        for i in range(self.parameter["T"]):
            
            for wordId in targetWordsId:

                # 1. "inflow" value has caluclated before end of step.
                if i == 0:
                    inflow = 100 + self._lexiconNetwork.nodes[wordId]["reservoir"]
                else:
                    inflow = self._lexiconNetwork.nodes[wordId]["inflow"]

                # 2. "reservoir" is representing activation value in each node
                reservoir = r * inflow

                # 3. Renew resvoir of current target node
                self._lexiconNetwork.nodes[wordId]["reservoir"] = reservoir

                # 4. "outflow" is all amount of following out to neighborhood nodes
                outflow = (1 - r) * inflow
                self._lexiconNetwork.nodes[wordId]["outflow"] = outflow
                #print(f"reservoir:{reservoir} outflow:{outflow} inflow:{inflow}")
                
                # 5. Calculation an renew to "inflow" value which each neighborhood node
                neighbors = self.renewNeighborsInflow(wordId) 
                nextTargetWordsId.append(neighbors)
                #print(f"amount of neighbor nodes:{len(neighbors)}")

            # 6. Renew to activation nodes at next step(next activation is defined by neighborhood nodes of all current target nodes)
            targetWordsId = util.flatList(nextTargetWordsId)
            nextTargetWordsId.clear()
            #print(f"amount of next target nodes:{len(targetWordsId)}")
                
        


        

