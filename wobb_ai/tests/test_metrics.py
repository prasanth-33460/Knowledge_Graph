import unittest
from final_evaluation.metrics import GraphEvaluation

class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.evaluator = GraphEvaluation()

    def test_evaluate_graph(self):
        true_graph_data = [{"nodes": ["John", "Acme Corp"], "edges": [("John", "Acme Corp")]}]
        predicted_graph_data = [{"nodes": ["John", "Acme Corp"], "edges": [("John", "Acme Corp")]}]
        results = self.evaluator.evaluate(true_graph_data, predicted_graph_data)
        self.assertIn("Graph_0", results)
        self.assertIn("edit_distance", results["Graph_0"])
        self.assertIn("centrality_difference", results["Graph_0"])