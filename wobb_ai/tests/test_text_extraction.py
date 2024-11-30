import unittest
from data_extraction.text_extraction import TextExtractor

class TestTextExtraction(unittest.TestCase):
    def setUp(self):
        self.extractor = TextExtractor()

    def test_extract_keywords(self):
        text = "The quick brown fox jumps over the lazy dog."
        keywords = self.extractor.extract_keywords(text)
        self.assertIn("fox", keywords)

    def test_extract_named_entities(self):
        text = "John Doe lives in New York."
        entities = self.extractor.extract_named_entities(text)
        self.assertIn("John Doe", entities)

if __name__ == "__main__":
    unittest.main()