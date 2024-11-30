import unittest
from graph_population.graph_query import GraphQuery

class TestGraphQuery(unittest.TestCase):
    def setUp(self):
        self.graph_query = GraphQuery()

    def test_query_graph(self):
        query = "MATCH (n) RETURN n"
        result = self.graph_query.query_graph(query)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)