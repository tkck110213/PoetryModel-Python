import CM
import MeCab
from utility.util import util
from tqdm import tqdm

class PoetoyCognitiveModelBySA:
    def __init__(self, parameter):
        self._wakati = MeCab.Tagger("-Owakati")
        self._parameter = parameter
        self._sam = CM.SpreadingActivationModel(self._parameter)
        self._util = util()
        

    def CognitivePoetory(self, courpusPath):
        with open(courpusPath, mode="r") as f:
            poetry = f.readlines()

        for i, line in enumerate(tqdm(poetry)):
            splitWords = self._wakati.parse(line).split()
            #print(splitWords)
            for word in splitWords:
                self._sam.activation(word)
            self._util.saveGraph(self._sam.getLexiconNetwork(), f"line{i}_network.gml")


            