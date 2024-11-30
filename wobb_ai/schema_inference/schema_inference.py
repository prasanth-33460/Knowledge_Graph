from collections import defaultdict
from typing import List, Dict

class SchemaInference:
    def infer_schema(self, entities: List[Dict], relationships: List[Dict]) -> Dict:
        schema = {
            "entities": self.infer_entities(entities),
            "relationships": self.infer_relationships(relationships),
            "properties": self.infer_properties(entities, relationships)
        }
        return schema

    def infer_entities(self, entities: List[Dict]) -> List[Dict]:
        entity_types = defaultdict(set)
        for entity in entities:
            entity_types[entity["type"]].add(entity["entity"])
        inferred_entities = [{"type": entity_type, "entities": list(entities)} for entity_type, entities in entity_types.items()]
        return inferred_entities

    def infer_relationships(self, relationships: List[Dict]) -> List[Dict]:
        relationship_types = defaultdict(list)
        for rel in relationships:
            relationship_types[rel["relation"]].append({
                "source": rel["source"],
                "target": rel["target"]
            })
        inferred_relationships = [{"relation": relation, "pairs": pairs} for relation, pairs in relationship_types.items()]
        return inferred_relationships

    def infer_properties(self, entities: List[Dict], relationships: List[Dict]) -> List[Dict]:
        properties = []
        for entity in entities:
            if entity["type"] == "PERSON":
                properties.append({
                    "entity": entity["entity"],
                    "type": entity["type"],
                    "properties": ["age", "occupation", "location"]
                })
            elif entity["type"] == "ORG":
                properties.append({
                    "entity": entity["entity"],
                    "type": entity["type"],
                    "properties": ["industry", "location", "CEO"]
                })
        for rel in relationships:
            properties.append({
                "relation": rel["relation"],
                "properties": ["strength", "duration"]  
            })
        return properties