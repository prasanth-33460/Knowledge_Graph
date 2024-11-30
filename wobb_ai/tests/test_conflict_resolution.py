import unittest
from schema_inference.conflict_resolution import ConflictResolution

class TestConflictResolution(unittest.TestCase):
    def setUp(self):
        self.resolver = ConflictResolution()

    def test_resolve_entity_conflicts(self):
        entities = [{"entity": "John", "type": "Person"}, {"entity": "John", "type": "Person"}]
        resolved_entities = self.resolver._resolve_entity_conflicts(entities)
        self.assertEqual(len(resolved_entities), 1)
        self.assertEqual(resolved_entities[0]["entity"], "John")

    def test_resolve_relationship_conflicts(self):
        relationships = [
            {"source": "John", "target": "Acme Corp", "relation": "works_at"},
            {"source": "John", "target": "Acme Corp", "relation": "works_at"}
        ]
        resolved_relationships = self.resolver._resolve_relationship_conflicts(relationships)
        self.assertEqual(len(resolved_relationships), 1)
        self.assertEqual(resolved_relationships[0]["source"], "John")