import unittest
from data_extraction.text_extraction import TextExtraction

class TestTextExtraction(unittest.TestCase):
    def setUp(self):
        self.extractor = TextExtraction()

    def test_extract_text(self):
        file_path = "/home/prxsxnthh/projects/wobb_AI/Prasanth_Thiagarajan - Resume.pdf"
        text = self.extractor.extract_text(file_path)
        self.assertGreater(len(text), 0)