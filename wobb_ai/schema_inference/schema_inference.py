import logging
from typing import Dict, List
from .conflict_resolution import ConflictResolution
from .entity_relationship_extraction import EntityRelationshipExtraction

logger = logging.getLogger(__name__)

class SchemaInference:
    def __init__(self):
        self.conflict_resolution = ConflictResolution()
        self.entity_relationship_extraction = EntityRelationshipExtraction()

    def infer_schema(self, entities: List[Dict], relationships: List[Dict]) -> Dict:
        try:
            logger.info("Starting schema inference process...")
            resolved_data = self.conflict_resolution.resolve_conflicts(entities, relationships)
            logger.info("Schema inference completed successfully.")
            return resolved_data
        except Exception as e:
            logger.error(f"Error occurred during schema inference: {e}")
            return {}