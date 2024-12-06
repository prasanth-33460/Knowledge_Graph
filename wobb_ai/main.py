import logging
from data_extraction.table_extraction import TableExtractor
from graph_population.knowledge_graph import KnowledgeGraph
from schema_inference.schema_inference import SchemaInference
from prompts.dynamic_prompts import DynamicPrompts
from utils.formatter import Formatter

# Configure logging to both console and file
log_file = "document_processing_output.log"  # Define the log file name
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler(log_file, mode='w')  # File output (overwrites each time)
    ]
)
logger = logging.getLogger(__name__)

class DocumentProcessingPipeline:
    def __init__(self, document_path):
        self.document_path = document_path
        self.table_extractor = TableExtractor(document_path)
        self.schema_inference = SchemaInference()
        self.knowledge_graph = KnowledgeGraph()
        self.dynamic_prompts = DynamicPrompts()

    def process(self):
        try:
            logger.info("Starting the document processing pipeline...")

            # Step 1: Extract tables from the document
            logger.info("Extracting tables from the document...")
            tables = self.table_extractor.extract_tables()
            if not tables:
                logger.warning("No tables found in the document. Exiting pipeline.")
                return

            # Step 2: Parse tables for potential drug names
            logger.info("Parsing extracted tables for drug names...")
            drug_names, parsed_table_data = self.table_extractor.parse_table_data(tables)
            if not drug_names:
                logger.warning("No drug names detected in the tables. Exiting pipeline.")
                return

            logger.info(f"Detected drug names: {drug_names}")
            logger.info(f"Parsed table data: {parsed_table_data}")

            # Step 3: Allow dynamic updates (user intervention for refining data)
            if self.dynamic_prompts.ask_for_updates():
                for drug_name in drug_names:
                    updated_name = self.dynamic_prompts.generate_entity_prompt(drug_name, "Drug")
                    if updated_name:
                        logger.info(f"Updated drug name: {updated_name}")

            # Step 4: Infer schema from the extracted and updated data
            logger.info("Inferring schema from the extracted data...")
            entities, relationships = self.schema_inference.infer_schema(drug_names, parsed_table_data)

            # Check if entities or relationships are empty
            if not entities or not relationships:
                logger.warning("No entities or relationships were inferred. Exiting pipeline.")
                return

            logger.info(f"Inferred entities: {entities}")
            logger.info(f"Inferred relationships: {relationships}")

            # Step 5: Allow updates to the schema inference
            self.dynamic_prompts.generate_schema_inference_prompt(entities, relationships)

            # Step 6: Populate knowledge graph
            logger.info("Populating the knowledge graph with inferred entities and relationships...")
            self.knowledge_graph.connect_to_neo4j()
            self.knowledge_graph.add_entities_and_relationships(entities, relationships)
            logger.info("Knowledge graph populated successfully.")
            self.knowledge_graph.close_connection()

            # Step 7: Clean and format the output before final logging
            logger.info("Cleaning and formatting the output...")
            formatted_entities = Formatter.clean_and_format_output(entities)
            formatted_relationships = Formatter.clean_and_format_output(relationships)

            logger.info(f"Formatted Entities: {formatted_entities}")
            logger.info(f"Formatted Relationships: {formatted_relationships}")

            logger.info("Document processing pipeline executed successfully.")
        except Exception as e:
            logger.error(f"Error in pipeline execution: {e}", exc_info=True)

if __name__ == "__main__":
    # Replace this path with your document's path
    DOCUMENT_PATH = "ASEAN.pdf"

    pipeline = DocumentProcessingPipeline(DOCUMENT_PATH)
    pipeline.process()
