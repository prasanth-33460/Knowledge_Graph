import logging
import pdfplumber

logger = logging.getLogger(__name__)

class TableExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_tables(self):
        """
        Extract tables from the given PDF file.
        """
        logger.info(f"Extracting tables from PDF: {self.pdf_path}")
        tables_data = []
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    logger.debug(f"Processing page {page_num}...")
                    tables = page.extract_tables()
                    if not tables:
                        logger.debug(f"No tables found on page {page_num}.")
                        continue

                    for table in tables:
                        logger.info(f"Table found on page {page_num}. Processing...")
                        structured_table = [row for row in table if any(row)]  # Remove empty rows
                        tables_data.append(structured_table)
        except Exception as e:
            logger.error(f"Error during table extraction: {e}", exc_info=True)

        logger.info(f"Extracted {len(tables_data)} tables from the PDF.")
        return tables_data

    def parse_table_data(self, tables):
        """
        Parse extracted tables to identify potential drug names and other data.
        """
        drug_names = set()
        parsed_data = []

        for table in tables:
            for row in table:
                for cell in row:
                    if isinstance(cell, str) and "drug" in cell.lower():
                        drug_names.add(cell.strip())
                    parsed_data.append(row)

        return list(drug_names), parsed_data
