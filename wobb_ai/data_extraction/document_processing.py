import os
from data_extraction.text_extraction import TextExtractor
from config import Config

class DocumentProcessor:
    def __init__(self):
        self.text_extractor = TextExtractor()

    def process(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_extension = file_path.split(".")[-1].lower()
        if file_extension not in Config.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file format: {file_extension}")

        return self.text_extractor.extract(file_path)
