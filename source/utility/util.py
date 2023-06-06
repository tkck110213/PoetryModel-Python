import networkx as nx
import os
import datetime
import itertools


class util:
    def __init__(self):
        self.dt_now = datetime.datetime.now()

    def saveGraph(self, graph, filename):
        #dirname = os.path.dirname()
        dirname = f"{os.path.expanduser('~')}/Project/PoetryModel/result/{self.dt_now.strftime('%Y-%m-%d-%H-%M-%S')}"

        if not os.path.isfile(dirname):
            os.makedirs(dirname, exist_ok=True)

        path = f"{dirname}/{filename}"

        nx.write_gml(graph, path)

def flatList(multiList, duplication=False):
    if duplication:
        return list(itertools.chain.from_iterable(multiList))
    else:
        return list(set(itertools.chain.from_iterable(multiList)))
