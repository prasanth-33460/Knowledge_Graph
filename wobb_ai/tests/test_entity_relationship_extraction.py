import unittest
from schema_inference.entity_relationship_extraction import EntityRelationshipExtractor

class TestEntityRelationshipExtraction(unittest.TestCase):
    def setUp(self):
        self.extractor = EntityRelationshipExtractor()

    def test_extract_relationships(self):
        text = "John works at Google."
        schema = self.extractor.extract(text)
        self.assertIn("John", schema["entities"])
        self.assertIn(("John", "works_at", "Google"), schema["relationships"])

if __name__ == "__main__":
    unittest.main()