import re
import pdfplumber

SECTION_PATTERN = re.compile(r"^P\d+")  # Pattern for section identification
PARAMETER_PATTERN = re.compile(r"^[A-Za-z\s]+:")  # Pattern for parameter identification

class TableExtractor:
    def __init__(self):
        pass
    
    def extract_tables(self, document_path):
        """
        Extract tables from a PDF document.

        Args:
            document_path (str): The path to the PDF document.

        Returns:
            list: A list of tables extracted from the document.
        """
        tables = []
        try:
            # Open the PDF document using pdfplumber
            with pdfplumber.open(document_path) as pdf:
                for page in pdf.pages:
                    # Extract tables from the page
                    table = page.extract_tables()
                    if table:
                        tables.append(table)
            return tables
        except Exception as e:
            print(f"Error extracting tables from the document: {e}")
            return []
        
    def parse_table_data(self, tables):
        """
        Parse the extracted tables into structured data.

        Args:
            tables (list): List of extracted tables.

        Returns:
            list: Parsed data, each containing a section and its parameters.
        """
        parsed_data = []
        for table in tables:
            section = self.extract_section(table)
            parameters = self.extract_parameters(table)
            
            if section and parameters:
                parsed_data.append({"section": section, "parameters": parameters})
        return parsed_data

    def extract_section(self, table):
        """
        Extract section information from the first row of the table.

        Args:
            table (list): The table to extract the section from.

        Returns:
            dict: The section data, or None if no section is found.
        """
        if not table:
            return None
        
        first_row = table[0]  # Get the first row of the table
        first_cell = first_row[0] if isinstance(first_row[0], str) else " ".join(map(str, first_row[0]))

        match = SECTION_PATTERN.match(first_cell)
        if match:
            section = match.group(0)
            return {"section": section}
        else:
            return None
        
    def extract_parameters(self, table):
        """
        Extract parameters from the table.

        Args:
            table (list): The table to extract parameters from.

        Returns:
            list: List of parameters extracted from the table.
        """
        parameters = []
        for row in table:
            param = self.extract_parameter(row)
            if param:
                parameters.append(param)
        return parameters
    
    def extract_parameter(self, row):
        """
        Extract a parameter from a row in the table.

        Args:
            row (list): A row in the table.

        Returns:
            dict: The parameter data, or None if no parameter is found.
        """
        if not row:
            return None
        
        # Ensure that the first element of the row is a string
        first_cell = row[0] if isinstance(row[0], str) else " ".join(map(str, row[0]))

        param_match = PARAMETER_PATTERN.match(first_cell)
        if param_match:
            parameter = param_match.group(0).strip(":")  # Remove colon if present
            components = self.extract_components(row)
            return {"parameter": parameter, "components": components}
        return None
    
    def extract_components(self, row):
        """
        Extract components and their requirements from a row in the table.

        Args:
            row (list): A row in the table.

        Returns:
            list: List of components and their requirements.
        """
        components = []
        for idx in range(1, len(row), 2):
            component = row[idx]
            requirement_str = row[idx + 1] if idx + 1 < len(row) else ""
            requirements = self.extract_requirements(requirement_str)
            components.append({"component": component, "requirements": requirements})
        return components
    
    def extract_requirements(self, requirement_str):
        """
        Extract requirements from a string.

        Args:
            requirement_str (str): The string containing requirements.

        Returns:
            dict: A dictionary of requirements.
        """
        requirements = {}
        reqs = requirement_str.split(",")
        for req in reqs:
            parts = req.split(":")
            if len(parts) == 2:
                requirements[parts[0].strip()] = parts[1].strip()
        return requirements
