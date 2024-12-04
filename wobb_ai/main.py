import logging
from data_extraction.document_processing import DocumentProcessor
from schema_inference.schema_inference import SchemaInference
from graph_population.knowledge_graph import KnowledgeGraph
from prompts.dynamic_prompts import DynamicPrompts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    try:
        logger.info("Starting the document processing pipeline...")
        document_processor = DocumentProcessor()
        schema_inferer = SchemaInference()
        graph = KnowledgeGraph()
        dynamic_prompts = DynamicPrompts()

        document_path = "/home/prxsxnthh/projects/wobb_AI/Knowledge_Graph/ASEAN.pdf"
        logger.info(f"Processing document: {document_path}")
        processed_data = document_processor.process(document_path)

        entities = processed_data.get("entities", [])
        relationships = processed_data.get("relationships", [])
        logger.info(f"Extracted entities: {entities}")
        logger.info(f"Extracted relationships: {relationships}")

        if not entities or not relationships:
            logger.warning("No entities or relationships extracted. Exiting pipeline.")
            return

        if dynamic_prompts.ask_for_updates():
            for entity in entities:
                updated_entity_info = dynamic_prompts.generate_entity_prompt(entity, "entity")
                if updated_entity_info:
                    logger.info(f"Updated entity information: {updated_entity_info}")

            for relationship in relationships:
                source, target, relation = relationship
                updated_relationship_info = dynamic_prompts.generate_relationship_prompt(source, target, relation)
                if updated_relationship_info:
                    logger.info(f"Updated relationship information: {updated_relationship_info}")

            for entity in entities:
                properties = ["name", "type", "description"]  # Example property list
                updated_properties = dynamic_prompts.generate_property_prompt(entity, "entity", properties)
                logger.info(f"Updated properties for entity '{entity}': {updated_properties}")
        else:
            logger.info("No updates were requested. Proceeding with default data.")

        inferred_schema = schema_inferer.infer_schema(entities, relationships)
        logger.info(f"Inferred schema: {inferred_schema}")

        graph.connect_to_neo4j()
        graph.add_entities_and_relationships(entities, relationships)
        logger.info("Knowledge graph populated successfully.")
        graph.close_connection()

        logger.info("Pipeline executed successfully.")

    except Exception as e:
        logger.error(f"Error in pipeline execution: {e}", exc_info=True)


if __name__ == "__main__":
    main()