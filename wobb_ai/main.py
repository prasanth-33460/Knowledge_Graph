import logging
from config import Config
from data_extraction.document_processing import DocumentProcessor
from schema_inference.schema_inference import SchemaInference
from graph_population.knowledge_graph import KnowledgeGraph
from final_evaluation.metrics import MetricsEvaluator
from prompts.dynamic_prompts import DynamicPrompts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Starting the document processing pipeline...")
        config = Config()
        document_processor = DocumentProcessor()
        schema_inferer = SchemaInference()
        graph = KnowledgeGraph()
        evaluator = MetricsEvaluator()
        dynamic_prompts = DynamicPrompts()  
        document_path = "/home/prxsxnthh/projects/wobb_AI/Prasanth_Thiagarajan - Resume.pdf"
        logger.info(f"Processing document: {document_path}")
        processed_data = document_processor.process(document_path)
        logger.info(f"Processed document data: {processed_data}")
        entities = processed_data.get("entities", [])
        relationships = processed_data.get("relationships", [])
        logger.info(f"Extracted entities: {entities}")
        logger.info(f"Extracted relationships: {relationships}")

        if not entities or not relationships:
            logger.warning("No entities or relationships extracted. Exiting pipeline.")
            return

        for entity in entities:
            entity_prompt = dynamic_prompts.generate_entity_prompt(entity, "entity")
            user_input = input(entity_prompt + " (Provide more details or 'skip'): ")
            if user_input.lower() != 'skip':
                logger.info(f"User provided details: {user_input}")
        
        for relationship in relationships:
            source, target, relation = relationship
            relationship_prompt = dynamic_prompts.generate_relationship_prompt(source, target, relation)
            user_input = input(relationship_prompt + " (Provide more details or 'skip'): ")
            if user_input.lower() != 'skip':
                logger.info(f"User provided details: {user_input}")
        inferred_schema = schema_inferer.infer_schema(entities, relationships)
        logger.info(f"Inferred schema: {inferred_schema}")
        graph.connect_to_neo4j()
        graph.add_entities_and_relationships(entities, relationships)
        logger.info("Knowledge graph populated successfully.")
        graph.close_connection()
        true_graph_data = [{"nodes": ["John", "Acme Corp"], "edges": [("John", "Acme Corp")]}]
        predicted_graph_data = [{"nodes": ["John", "Acme Corp"], "edges": [("John", "Acme Corp")]}]
        evaluation_results = evaluator.evaluate_graph_population(true_graph_data, predicted_graph_data)
        logger.info(f"Evaluation results: {evaluation_results}")
        logger.info("Pipeline executed successfully.")

    except Exception as e:
        logger.error(f"Error in pipeline execution: {e}", exc_info=True)

if __name__ == "__main__":
    main()