import unittest
from evaluation.metrics import Metrics

class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.metrics = Metrics()

    def test_evaluate(self):
        schema = {"entities": ["A", "B"], "relationships": [("A", "related_to", "B")]}
        entities = ["A", "B"]
        relationships = [("A", "related_to", "B")]
        evaluation = self.metrics.evaluate(schema, entities, relationships)
        self.assertEqual(evaluation["completeness"], 1.0)
        self.assertEqual(evaluation["accuracy"], 1.0)

if __name__ == "__main__":
    unittest.main()