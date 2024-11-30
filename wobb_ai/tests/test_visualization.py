import unittest
from graph_population.visualization import GraphVisualization

class TestVisualization(unittest.TestCase):
    def setUp(self):
        self.visualizer = GraphVisualization()

    def test_visualize_graph(self):
        graph_data = {"nodes": ["John", "Acme Corp"], "edges": [("John", "Acme Corp")]}
        visualization = self.visualizer.visualize(graph_data)
        self.assertIsNotNone(visualization)