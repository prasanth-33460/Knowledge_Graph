import matplotlib.pyplot as plt
from pyvis.network import Network

class Visualization:
    def render(self, nodes, edges):
        net = Network(notebook=True)
        for node in nodes:
            net.add_node(node)
        for edge in edges:
            net.add_edge(*edge)
        net.show("graph.html")