import logging
from typing import List, Dict
logger = logging.getLogger(__name__)

class EntityRelationshipExtraction:
    def __init__(self):
        pass

    def extract_entities(self, document: str) -> List[Dict]:
        entities = []
        for word in document.split():
            if word[0].isupper():  
                entities.append({"entity": word, "type": "UNKNOWN"})
        logger.debug(f"Extracted entities: {entities}")
        return entities

    def extract_relationships(self, document: str) -> List[Dict]:
        relationships = []
        words = document.split()
        for i in range(len(words) - 1):
            if words[i][0].isupper() and words[i + 1][0].isupper():
                relationships.append({
                    "source": words[i],
                    "target": words[i + 1],
                    "relation": "related_to"
                })
        logger.debug(f"Extracted relationships: {relationships}")
        return relationships