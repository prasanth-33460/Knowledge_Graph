import unittest
from schema_inference.conflict_resolution import ConflictResolution

class TestConflictResolution(unittest.TestCase):
    def setUp(self):
        self.resolver = ConflictResolution()

    def test_resolve_conflicts(self):
        schema = {"entities": ["A"], "relationships": [("A", "related_to", "B")]}
        new_schema = {"entities": ["B"], "relationships": [("B", "related_to", "C")]}
        resolved = self.resolver.resolve(schema, new_schema)
        self.assertIn("C", resolved["entities"])
        self.assertIn(("B", "related_to", "C"), resolved["relationships"])

if __name__ == "__main__":
    unittest.main()