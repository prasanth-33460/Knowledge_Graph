import unittest
from graph_population.knowledge_graph import KnowledgeGraph

class TestKnowledgeGraph(unittest.TestCase):
    def setUp(self):
        self.graph = KnowledgeGraph()

    def test_add_entity(self):
        self.graph.add_entity("Person", {"name": "John"})
        entities = self.graph.list_entities()
        self.assertIn("John", [e["name"] for e in entities])

    def test_add_relationship(self):
        self.graph.add_entity("Person", {"name": "John"})
        self.graph.add_entity("Company", {"name": "Google"})
        self.graph.add_relationship("John", "works_at", "Google")
        relationships = self.graph.list_relationships()
        self.assertIn(("John", "works_at", "Google"), relationships)

if __name__ == "__main__":
    unittest.main()