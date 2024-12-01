import os
import logging
from data_extraction.parsers.pdf_parser import PDFParser
from data_extraction.parsers.docx_parser import DocxParser
from data_extraction.parsers.image_parser import ImageParser
from data_extraction.parsers.json_parser import JSONParser
from data_extraction.parsers.csv_parser import CSVParser

logger = logging.getLogger(__name__)

class TextExtractor:
    def __init__(self):
        self.parsers = {
            "pdf": PDFParser(),
            "docx": DocxParser(),
            "jpg": ImageParser(),
            "jpeg": ImageParser(), 
            "png": ImageParser(),
            "json": JSONParser(),
            "csv": CSVParser(),
        }

    def extract(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = file_path.split(".")[-1].lower()
        logger.info(f"Processing file: {file_path} with extension: {file_extension}")

        if file_extension in self.parsers:
            parser = self.parsers[file_extension]
            try:
                extracted_data = parser.parse(file_path)
                logger.info(f"Successfully parsed {file_path} using {parser.__class__.__name__}")
                return extracted_data
            except Exception as e:
                logger.error(f"Error parsing file {file_path}: {e}")
                raise ValueError(f"Failed to parse file: {file_path}. Error: {e}")
        else:
            logger.error(f"No parser available for format: {file_extension}")
            raise ValueError(f"Unsupported file format: {file_extension}")