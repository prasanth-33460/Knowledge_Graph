import unittest
from graph_population.visualization import Visualization

class TestVisualization(unittest.TestCase):
    def setUp(self):
        self.visualizer = Visualization()

    def test_render_graph(self):
        nodes = ["Node1", "Node2"]
        edges = [("Node1", "Node2")]
        self.visualizer.render(nodes, edges)
        self.assertTrue(True)  

if __name__ == "__main__":
    unittest.main()