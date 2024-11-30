import unittest
from schema_inference.schema_inference import SchemaInference

class TestSchemaInference(unittest.TestCase):
    def setUp(self):
        self.schema_inferer = SchemaInference()

    def test_infer_schema(self):
        document = "John works at Acme Corp."
        inferred_schema = self.schema_inferer.infer_schema(document)
        self.assertIn("entities", inferred_schema)
        self.assertIn("relationships", inferred_schema)