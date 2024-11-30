import logging
from config import Config
from data_extraction.document_processing import DocumentProcessor
from schema_inference.schema_inference import SchemaInference
from schema_inference.entity_relationship_extraction import EntityRelationshipExtractor
from graph_population.knowledge_graph import KnowledgeGraph
from prompts.dynamic_prompts import DynamicPrompts
from evaluation.metrics import Metrics

logging.basicConfig(filename=Config.LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    logging.info("Starting the Knowledge Graph Construction System...")
    
    document_processor = DocumentProcessor()
    schema_inference = SchemaInference()
    entity_extractor = EntityRelationshipExtractor()
    knowledge_graph = KnowledgeGraph()
    dynamic_prompts = DynamicPrompts()
    metrics = Metrics()

    document_path = "sample_input.pdf"
    extracted_text = document_processor.process(document_path)

    entities, relationships = entity_extractor.extract(extracted_text)

    schema = schema_inference.infer_schema(entities, relationships)

    refined_schema = dynamic_prompts.refine_schema(schema)

    knowledge_graph.populate(refined_schema, entities, relationships)

    evaluation_results = metrics.evaluate(refined_schema, entities, relationships)
    logging.info(f"Evaluation Results: {evaluation_results}")

    logging.info("Knowledge Graph Construction completed successfully!")

if __name__ == "__main__":
    main()