from PyPDF2 import PdfReader
import pdfplumber

class PDFParser:
    def parse(self, file_path):
        reader = PdfReader(file_path)
        text = " "
        for page in reader.pages:
            text += page.extract_text()
        return text