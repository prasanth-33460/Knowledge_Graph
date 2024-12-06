import logging
from data_extraction.table_extraction import TableExtractor
from graph_population.knowledge_graph import KnowledgeGraph
from schema_inference.schema_inference import SchemaInference
from prompts.dynamic_prompts import DynamicPrompts

# Configure logging
log_file = "wobb_ai/output/document_processing_output.log"
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file, mode='w')
    ]
)
logger = logging.getLogger(__name__)

class DocumentProcessingPipeline:
    def __init__(self, document_path, output_file="wobb_ai/output/pipeline_output.txt"):
        self.document_path = document_path
        self.output_file = output_file
        self.table_extractor = TableExtractor()
        self.schema_inference = SchemaInference()
        self.knowledge_graph = KnowledgeGraph()
        self.dynamic_prompts = DynamicPrompts()

    def save_output(self, sections):
        """
        Save output in the requested format to a file.
        """
        try:
            with open(self.output_file, 'w') as file:
                for section in sections:
                    file.write(f"Section: {section['section']}\n")
                    for parameter in section['parameters']:
                        file.write(f"  Parameter: {parameter['parameter']}\n")
                        for comp in parameter['components']:
                            file.write(f"    Component: {comp['component']}\n")
                            file.write(f"    Requirements:\n")
                            for key, value in comp['requirements'].items():
                                if value:  # Only show if there's a tick mark
                                    file.write(f"      - {key}: {value}\n")
                    file.write("-" * 40 + "\n")
            logger.info(f"Output successfully saved to {self.output_file}")
        except Exception as e:
            logger.error(f"Failed to save output: {e}", exc_info=True)

    def process(self):
        try:
            logger.info("Starting the document processing pipeline...")

            # Step 1: Extract tables from the document
            logger.info("Extracting tables from the document...")
            tables = self.table_extractor.extract_tables(self.document_path)
            if not tables:
                logger.warning("No tables found in the document. Exiting pipeline.")
                return

            # Step 2: Parse tables for sections, descriptions, and requirements
            logger.info("Parsing extracted tables...")
            parsed_table_data = self.table_extractor.parse_table_data(tables)
            if not parsed_table_data:
                logger.warning("No structured data found in the tables. Exiting pipeline.")
                return

            logger.info(f"Parsed data:\n{parsed_table_data}")

            # Log and prepare output
            sections = []
            for section_data in parsed_table_data:
                logger.info(f"Parsed Section:\n"
                            f"Section: {section_data['section']}\n"
                            f"Parameters: {len(section_data['parameters'])}\n"
                            f"{'-' * 40}")
                sections.append(section_data)

            # Save the output in the specified format
            self.save_output(sections)

            logger.info("Document processing pipeline executed successfully.")
        except Exception as e:
            logger.error(f"Error in pipeline execution: {e}", exc_info=True)

if __name__ == "__main__":
    DOCUMENT_PATH = "ASEAN.pdf"
    OUTPUT_FILE = "wobb_ai/output/pipeline_output.txt"

    pipeline = DocumentProcessingPipeline(DOCUMENT_PATH, OUTPUT_FILE)
    pipeline.process()
