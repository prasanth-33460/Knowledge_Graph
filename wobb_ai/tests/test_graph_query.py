import unittest
from graph_population.graph_query import GraphQuery

class TestGraphQuery(unittest.TestCase):
    def setUp(self):
        self.query = GraphQuery()

    def test_execute_query(self):
        query = "MATCH (n) RETURN n LIMIT 1"
        results = self.query.execute_query(query)
        self.assertIsInstance(results, list)

if __name__ == "__main__":
    unittest.main()