import logging
from config import Config
from data_extraction.document_processing import DocumentProcessor
from schema_inference.schema_inference import SchemaInference
from graph_population.knowledge_graph import KnowledgeGraph
from final_evaluation.metrics import MetricsEvaluator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        config = Config()

        document_processor = DocumentProcessor()
        document = "/home/prxsxnthh/projects/wobb_AI/Prasanth_Thiagarajan - Resume.pdf"
        processed_data = document_processor.process(document)
        logger.info(f"Processed document data: {processed_data}")

        entities = processed_data.get("entities", [])
        relationships = processed_data.get("relationships", [])

        schema_inferer = SchemaInference()
        inferred_schema = schema_inferer.infer_schema(entities, relationships)
        logger.info(f"Inferred schema: {inferred_schema}")

        graph = KnowledgeGraph(config.graph_db_uri, config.graph_username, config.graph_password)
        graph.add_entities_and_relationships(entities, relationships)
        logger.info("Graph populated with data.")

        evaluator = MetricsEvaluator()
        true_graph_data = [{"nodes": ["John", "Acme Corp"], "edges": [("John", "Acme Corp")]}]
        predicted_graph_data = [{"nodes": ["John", "Acme Corp"], "edges": [("John", "Acme Corp")]}]
        evaluation_results = evaluator.evaluate(true_graph_data, predicted_graph_data)
        logger.info(f"Evaluation results: {evaluation_results}")

    except Exception as e:
        logger.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()