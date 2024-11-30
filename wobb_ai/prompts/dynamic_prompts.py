import logging
from typing import List, Dict
logger = logging.getLogger(__name__)

class DynamicPrompts:
    def __init__(self):
        pass

    def generate_entity_prompt(self, entity: str, entity_type: str) -> str:
        prompt = f"Please provide more information about the {entity_type} named {entity}."
        logger.debug(f"Generated entity prompt: {prompt}")
        return prompt

    def generate_relationship_prompt(self, source_entity: str, target_entity: str, relation: str) -> str:
        prompt = f"What is the relationship between {source_entity} and {target_entity} regarding {relation}?"
        logger.debug(f"Generated relationship prompt: {prompt}")
        return prompt

    def generate_property_prompt(self, entity: str, entity_type: str, properties: List[str]) -> str:
        properties_str = ', '.join(properties)
        prompt = f"Can you provide the following properties for the {entity_type} named {entity}? {properties_str}"
        logger.debug(f"Generated property prompt: {prompt}")
        return prompt

    def generate_query_prompt(self, query_type: str, filters: Dict[str, str]) -> str:
        query_conditions = " AND ".join([f"{key}={value}" for key, value in filters.items()])
        prompt = f"Generate a {query_type} query with conditions: {query_conditions}"
        logger.debug(f"Generated query prompt: {prompt}")
        return prompt

    def generate_schema_inference_prompt(self, entities: List[str], relationships: List[str]) -> str:
        entity_list = ', '.join(entities)
        relationship_list = ', '.join(relationships)
        prompt = f"Please infer the schema based on the following entities: {entity_list}, and relationships: {relationship_list}."
        logger.debug(f"Generated schema inference prompt: {prompt}")
        return prompt