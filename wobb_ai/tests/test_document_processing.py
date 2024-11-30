import unittest
from data_extraction.document_processing import DocumentProcessor

class TestDocumentProcessor(unittest.TestCase):

    def test_pdf_extraction(self):
        processor = DocumentProcessor('sample.pdf')
        text = processor.extract_text()
        self.assertTrue(len(text) > 0, "Text extraction from PDF failed.")
    def test_docx_extraction(self):
        processor = DocumentProcessor('sample.docx')
        text = processor.extract_text()
        self.assertTrue(len(text) > 0, "Text extraction from DOCX failed.")

    def test_txt_extraction(self):
        processor = DocumentProcessor('sample.txt')
        text = processor.extract_text()
        self.assertTrue(len(text) > 0, "Text extraction from TXT failed.")

if __name__ == '__main__':
    unittest.main()
