import MeCab
import json
from PCM import PoetoyCognitiveModelBySA
import sys
import os

def main(parameterPath):
    parameter = json.load(open(parameterPath))["parameter"]
    pcm = PoetoyCognitiveModelBySA(parameter)
    pcm.CognitivePoetory(f'{os.path.expanduser("~")}/Project/Resource/poetry_corpus/poetry1.txt')

main(sys.argv[1])