from wobb_ai.data_extraction.parsers.pdf_parser import PDFParser
from wobb_ai.data_extraction.parsers.image_parser import ImageParser

class PDFImageExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.pdf_parser = PDFParser()
        self.image_parser = ImageParser()

    def extract_data(self):
        """Extracts data from a PDF or image."""
        if self.file_path.endswith('.pdf'):
            return self._extract_from_pdf()
        elif self.file_path.endswith(('.jpg', '.jpeg', '.png')):
            return self._extract_from_image()
        else:
            raise ValueError("Unsupported file type!")

    def _extract_from_pdf(self):
        """Extract tables from a PDF file."""
        return self.pdf_parser.extract_table_from_pdf(self.file_path)

    def _extract_from_image(self):
        """Extract text from an image file."""
        return self.image_parser.parse(self.file_path)
