from data_extraction.parsers.pdf_parser import PDFParser
from data_extraction.parsers.docx_parser import DocxParser
from data_extraction.parsers.image_parser import ImageParser
from data_extraction.parsers.json_parser import JSONParser
from data_extraction.parsers.csv_parser import CSVParser

class TextExtractor:
    def __init__(self):
        self.parsers = {
            "pdf": PDFParser(),
            "docx": DocxParser(),
            "jpg": ImageParser(),
            "png": ImageParser(),
            "json": JSONParser(),
            "csv": CSVParser()
        }

    def extract(self, file_path):
        file_extension = file_path.split(".")[-1].lower()
        if file_extension in self.parsers:
            return self.parsers[file_extension].parse(file_path)
        else:
            raise ValueError(f"No parser available for format: {file_extension}")