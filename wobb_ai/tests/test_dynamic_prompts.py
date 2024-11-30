import unittest
from prompts.dynamic_prompts import DynamicPrompts

class TestDynamicPrompts(unittest.TestCase):
    def setUp(self):
        self.prompts = DynamicPrompts()

    def test_refine_schema(self):
        schema = {"entities": ["A"], "relationships": []}
        refined_schema = self.prompts.refine_schema(schema)
        self.assertTrue(refined_schema["entities"])

if __name__ == "__main__":
    unittest.main()