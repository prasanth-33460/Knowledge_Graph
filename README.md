Knowledge Graph Construction and Evaluation
Overview
This project provides an end-to-end pipeline for constructing a knowledge graph from structured documents and evaluating the quality of the graph using accuracy and completeness metrics. It uses Neo4j for graph storage and provides various modules for document extraction, schema inference, and graph population. The evaluation process is enhanced by querying the Neo4j database to compare inferred entities and relationships with the ground truth.

The Metrics class in this project calculates the accuracy and completeness of the inferred knowledge graph by comparing it to the data stored in Neo4j.

Setup Instructions

1. Clone the Repository
Clone the repository to your local machine:
git clone <git@github.com>:prasanth-33460/wobb__AI.git
cd wobb_AI

2. Install Dependencies
Ensure you have Python 3.7+ installed, then install the required dependencies using Poetry (recommended) or pip.

Using Poetry:
Poetry is a dependency manager for Python that simplifies the installation of dependencies.
--> Install Poetry (if not already installed):
curl -sSL <https://install.python-poetry.org> | python3 -
--> Install project dependencies:
poetry install
-->Using pip:
Alternatively, you can install dependencies directly using pip:
pip install -r requirements.txt
3. Neo4j Setup
This project uses Neo4j to store and query the knowledge graph. You need to have a running Neo4j instance:

Install Neo4j Community Edition from Neo4j's official website.
Start Neo4j on your local machine (default port 7687 for the bolt protocol).
You can use the default credentials (neo4j / password) for local setup, or configure them according to your environment.

Configuration
Before running the evaluation or other components, make sure to configure the Neo4j connection URI in the Metrics class:
neo4j_uri = "bolt://localhost:7687"  # Adjust based on your Neo4j setup
You also need to specify the ground truth schema, which will be used to calculate accuracy and completeness metrics.

Usage
Running the Evaluation
You can evaluate the knowledge graph's accuracy and completeness by running the Metrics class. This will compare the inferred entities and relationships against the ground truth stored in your Neo4j instance.

Example:

from wobb_ai.evaluation.metrics import Metrics
neo4j_uri = "bolt://localhost:7687"  # Adjust based on your setup
ground_truth_schema = {
    "entities": ["John", "Google", "Mary", "Microsoft"],
    "relationships": [
        {"source": "John", "relation": "works_with", "target": "Google"},
        {"source": "Mary", "relation": "works_with", "target": "Microsoft"}
    ]
}

metrics = Metrics(neo4j_uri, ground_truth_schema)

inferred_entities = [
    {"entity": "John", "type": "PERSON"},
    {"entity": "Google", "type": "ORG"},
    {"entity": "Mary", "type": "PERSON"},
    {"entity": "Microsoft", "type": "ORG"}
]

inferred_relationships = [
    {"source": "John", "relation": "works_with", "target": "Google"},
    {"source": "Mary", "relation": "works_with", "target": "Microsoft"}
]

result = metrics.evaluate(None, inferred_entities, inferred_relationships)
print(result)

Expected Output:

{
    "accuracy": 100.0,
    "completeness": 100.0
}

Customizing the Evaluation
The accuracy metric reflects how many inferred entities and relationships match the ground truth stored in the Neo4j database.
The completeness metric indicates how many of the ground truth entities and relationships are correctly identified in the inferred knowledge graph.Testing
You can run the tests to verify the correctness of each module in the project.

--> Install pytest if not already installed:
            pip install pytest
--> Run the tests:
            pytest tests/

Contributing
Contributions to this project are welcome! If you'd like to improve the functionality, fix bugs, or add new features, feel free to submit a pull request.

Final Notes
This project provides a foundational pipeline for knowledge graph construction and evaluation using Neo4j. It can be adapted for various types of structured documents, with easy integration for future improvements and more complex evaluation metrics.
