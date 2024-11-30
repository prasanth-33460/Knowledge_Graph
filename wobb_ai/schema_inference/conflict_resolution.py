import logging
from typing import List, Dict
logger = logging.getLogger(__name__)

class ConflictResolution:
    def __init__(self):
        pass

    def resolve_conflicts(self, entities: List[Dict], relationships: List[Dict]) -> Dict:
        try:
            logger.info("Resolving conflicts in the entities and relationships...")
            resolved_entities = self._resolve_entity_conflicts(entities)
            resolved_relationships = self._resolve_relationship_conflicts(relationships)
            logger.info("Conflict resolution completed successfully.")
            return {
                "entities": resolved_entities,
                "relationships": resolved_relationships
            }
        except Exception as e:
            logger.error(f"Error occurred during conflict resolution: {e}")
            return {}

    def _resolve_entity_conflicts(self, entities: List[Dict]) -> List[Dict]:
        entity_names = {}
        resolved_entities = []
        for entity in entities:
            entity_name = entity.get("entity")
            if entity_name in entity_names:
                entity_names[entity_name].append(entity)
            else:
                entity_names[entity_name] = [entity]
        for name, entity_list in entity_names.items():
            if len(entity_list) == 1:
                resolved_entities.append(entity_list[0])
            else:
                resolved_entities.append(max(entity_list, key=lambda x: len(x)))
        return resolved_entities

    def _resolve_relationship_conflicts(self, relationships: List[Dict]) -> List[Dict]:
        relationship_map = {}
        resolved_relationships = []
        for rel in relationships:
            key = (rel.get("source"), rel.get("target"), rel.get("relation"))
            if key in relationship_map:
                relationship_map[key].append(rel)
            else:
                relationship_map[key] = [rel]
        for key, rel_list in relationship_map.items():
            if len(rel_list) == 1:
                resolved_relationships.append(rel_list[0]) 
            else:
                resolved_relationships.append(max(rel_list, key=lambda x: len(x)))
        return resolved_relationships