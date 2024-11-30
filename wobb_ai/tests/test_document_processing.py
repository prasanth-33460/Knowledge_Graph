import unittest
from data_extraction.document_processing import DocumentProcessing

class TestDocumentProcessing(unittest.TestCase):
    def setUp(self):
        self.processor = DocumentProcessing()

    def test_process_document(self):
        document = "John works at Acme Corp."
        processed_data = self.processor.process_document(document)
        self.assertIsInstance(processed_data, dict)
        self.assertIn("entities", processed_data)
        self.assertIn("relationships", processed_data)