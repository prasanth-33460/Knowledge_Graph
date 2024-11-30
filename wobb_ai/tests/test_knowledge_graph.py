import unittest
from graph_population.knowledge_graph import KnowledgeGraph

class TestKnowledgeGraph(unittest.TestCase):
    def setUp(self):
        self.graph = KnowledgeGraph()

    def test_add_node(self):
        self.graph.add_node("John", {"type": "Person"})
        node = self.graph.get_node("John")
        self.assertIsNotNone(node)
        self.assertEqual(node["type"], "Person")

    def test_add_edge(self):
        self.graph.add_edge("John", "Acme Corp", {"relation": "works_at"})
        edge = self.graph.get_edge("John", "Acme Corp")
        self.assertIsNotNone(edge)
        self.assertEqual(edge["relation"], "works_at")