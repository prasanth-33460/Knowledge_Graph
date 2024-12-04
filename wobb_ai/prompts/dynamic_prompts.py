import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class DynamicPrompts:
    def __init__(self):
        pass

    def ask_for_updates(self) -> bool:
        user_input = input("Do you want to update any information? (yes/no): ").strip().lower()
        if user_input == "yes":
            logger.info("User opted to update information.")
            return True
        elif user_input == "no":
            logger.info("User chose not to update information.")
            return False
        else:
            logger.warning(f"Invalid input: {user_input}. Assuming 'no'.")
            return False

    def generate_entity_prompt(self, entity: str, entity_type: str) -> str:
        user_input = input(f"Do you want to update the entity '{entity}'? (yes/no): ").strip().lower()
        if user_input == "yes":
            prompt = f"Please provide updated information about the {entity_type} named '{entity}': "
            logger.info(f"Asking for updated details for entity: {entity}")
            return input(prompt)
        else:
            logger.info(f"No updates provided for entity: {entity}")
            return ""

    def generate_relationship_prompt(self, source_entity: str, target_entity: str, relation: str) -> str:
        user_input = input(f"Do you want to update the relationship between '{source_entity}' and '{target_entity}' regarding '{relation}'? (yes/no): ").strip().lower()
        if user_input == "yes":
            prompt = f"Please provide updated information for the relationship between '{source_entity}' and '{target_entity}' regarding '{relation}': "
            logger.info(f"Asking for updated details for relationship: {source_entity} -> {relation} -> {target_entity}")
            return input(prompt)
        else:
            logger.info(f"No updates provided for relationship: {source_entity} -> {relation} -> {target_entity}")
            return ""

    def generate_property_prompt(self, entity: str, entity_type: str, properties: List[str]) -> Dict[str, str]:
        user_input = input(f"Do you want to update properties for the {entity_type} named '{entity}'? (yes/no): ").strip().lower()
        updated_properties = {}
        if user_input == "yes":
            for prop in properties:
                updated_value = input(f"Please provide the updated value for property '{prop}': ").strip()
                if updated_value:
                    updated_properties[prop] = updated_value
                    logger.info(f"Updated property '{prop}' for entity '{entity}' with value: {updated_value}")
        else:
            logger.info(f"No updates provided for properties of entity: {entity}")
        return updated_properties

    def generate_schema_inference_prompt(self, entities: List[str], relationships: List[str]) -> None:
        user_input = input("Do you want to modify the schema inference data? (yes/no): ").strip().lower()
        if user_input == "yes":
            for entity in entities:
                logger.info(f"Allowing updates for entity '{entity}' during schema inference.")
                self.generate_entity_prompt(entity, "entity")
            for source, target, relation in relationships:
                logger.info(f"Allowing updates for relationship '{source} -> {relation} -> {target}' during schema inference.")
                self.generate_relationship_prompt(source, target, relation)
        else:
            logger.info("Skipping schema inference updates.")