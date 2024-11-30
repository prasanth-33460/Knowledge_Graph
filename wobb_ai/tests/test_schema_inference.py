import unittest
from schema_inference.schema_inference import SchemaInference

class TestSchemaInference(unittest.TestCase):
    def setUp(self):
        self.inference = SchemaInference()

    def test_infer_schema(self):
        text = "John is a software engineer at Google."
        schema = self.inference.infer([text])
        self.assertIn("John", schema["entities"])
        self.assertIn(("John", "works_at", "Google"), schema["relationships"])

if __name__ == "__main__":
    unittest.main()