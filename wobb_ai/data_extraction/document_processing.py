import os
from data_extraction.text_extraction import TextExtractor
from config import Config
import logging

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        self.text_extractor = TextExtractor()

    def process(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        logger.info(f"Processing file: {file_path}")

        extracted_text = self.text_extractor.extract(file_path)
        logger.info(f"Extracted text: {extracted_text}")

        entities = self.extract_entities(extracted_text)
        relationships = self.extract_relationships(entities)

        return {"text": extracted_text, "entities": entities, "relationships": relationships}

    def extract_entities(self, text):
        entities = []
        for word in text.split():
            if word.istitle():  
                entities.append({"name": word, "type": "ProperNoun"})
        logger.info(f"Extracted entities: {entities}")
        return entities

    def extract_relationships(self, entities):
        relationships = []
        if len(entities) > 1:
            for i in range(len(entities) - 1):
                relationships.append({
                    "source": entities[i]["name"],
                    "target": entities[i + 1]["name"],
                    "type": "RelatedTo"
                })
        logger.info(f"Extracted relationships: {relationships}")
        return relationships