# Wobb AI: Document Processing and Knowledge Graph Pipeline

This project involves document processing, schema inference, and knowledge graph population using data extracted from documents. The goal is to process various documents, extract entities, relationships, and properties, infer a schema, and populate a Neo4j graph. The project also includes a Streamlit web app for dynamic interaction, allowing users to see the flow of document processing and explore the knowledge graph.

## Features

- **Document Processing**: Extract entities, relationships, and properties from different document formats (PDF, DOCX, etc.).
- **Schema Inference**: Infer a schema based on the extracted data, including entities and relationships.
- **Knowledge Graph Population**: Add entities and relationships to a Neo4j database.
- **Dynamic Prompts**: Generate dynamic prompts for schema refinement, entity relationships, and graph updates.
- **Streamlit App**: Provides an interactive web interface to view and manage the pipeline process and Neo4j graph output.

## Requirements

- Python 3.7 or later
- Neo4j database (local or cloud instance)
- Streamlit for web interface

## Setup Instructions

Follow these steps to set up and run the project:

### 1. Clone the repository
First, clone the project repository:

git clone https://github.com/prasanth-33460/wobb__AI.git
cd wobb-ai

2. Install dependencies
Create a virtual environment and install the required packages using pip:

Option 1: Using requirements.txt
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt

Option 2: Using Poetry (if preferred)
poetry init
poetry install $(cat requirements.txt)

3. Configure Neo4j
Make sure you have a Neo4j instance running. You can either set up a local Neo4j instance or use Neo4j Aura (cloud service).

Local Neo4j: Download and install Neo4j Desktop or run a Docker container.
Neo4j Aura: Create a free instance on Neo4j Aura.
Once your Neo4j instance is running, make sure to update the config.py file with your Neo4j connection details (username, password, and URI).

Example of config.py:
class Config:
    NE4J_URI = "neo4j://localhost:7687"  # Update with your Neo4j URI
    NE4J_USERNAME = "neo4j" 
    NE4J_PASSWORD = "your_password" #update with your neo4j password

4. Run the Pipeline
To run the document processing and knowledge graph pipeline, simply run the following:
python wobb_ai/main.py

This will:

Process the input document (e.g., Resume.pdf).
Extract entities, relationships, and properties.
Infer a schema and populate the Neo4j graph.

5. Run the Streamlit Web Interface
To view the results in the web interface, run the Streamlit app:
streamlit run wobb_ai/app.py

This will open a local Streamlit app where you can:

View the document processing steps.
Generate dynamic prompts for schema inference.
View the populated knowledge graph from Neo4j.

6. Testing
Run the tests using:
pytest/
...following

Troubleshooting
Neo4j connection issues: Double-check the URI, username, and password in config.py. If you're using a remote instance, ensure your firewall or cloud security settings allow the connection.
Missing dependencies: If you encounter missing dependencies, run pip install -r requirements.txt again to ensure all required packages are installed.
Streamlit app not running: Ensure the correct port is available (Streamlit defaults to port 8501). If it's taken, run Streamlit on a different port:
streamlit run streamlit_app/app.py --server.port 8502
