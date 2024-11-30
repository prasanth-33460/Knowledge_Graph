import unittest
from schema_inference.entity_relationship_extraction import EntityRelationshipExtraction

class TestEntityRelationshipExtraction(unittest.TestCase):
    def setUp(self):
        self.extractor = EntityRelationshipExtraction()

    def test_extract_entities(self):
        document = "John works at Acme Corp."
        entities = self.extractor.extract_entities(document)
        self.assertGreater(len(entities), 0)
        self.assertEqual(entities[0]["entity"], "John")

    def test_extract_relationships(self):
        document = "John works at Acme Corp."
        relationships = self.extractor.extract_relationships(document)
        self.assertGreater(len(relationships), 0)
        self.assertEqual(relationships[0]["relation"], "related_to")