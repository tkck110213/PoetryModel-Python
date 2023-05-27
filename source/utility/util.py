import networkx as nx
import os
import datetime

class util:
    def __init__(self):
        self.dt_now = datetime.datetime.now()

    def saveGraph(self, graph, filename):
        #dirname = os.path.dirname()
        dirname = "../result/" + self.dt_now.strftime('%Y-%m-%d-%H-%M-%S')

        if not os.path.isfile(dirname):
            os.makedirs(dirname, exist_ok=True)

        path = f"{dirname}/{filename}"

        nx.write_gml(graph, path)