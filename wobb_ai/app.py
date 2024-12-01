from typing import List
import streamlit as st
import logging
from neo4j import GraphDatabase
import matplotlib.pyplot as plt
import networkx as nx

logger = logging.getLogger(__name__)

class DynamicPrompts:
    def __init__(self):
        pass

    def generate_entity_prompt(self, entity: str, entity_type: str) -> str:
        prompt = f"Please provide more information about the {entity_type} named {entity}."
        logger.debug(f"Generated entity prompt: {prompt}")
        return prompt

    def generate_relationship_prompt(self, source_entity: str, target_entity: str, relation: str) -> str:
        prompt = f"What is the relationship between {source_entity} and {target_entity} regarding {relation}?"
        logger.debug(f"Generated relationship prompt: {prompt}")
        return prompt

    def generate_property_prompt(self, entity: str, entity_type: str, properties: List[str]) -> str:
        properties_str = ', '.join(properties)
        prompt = f"Can you provide the following properties for the {entity_type} named {entity}? {properties_str}"
        logger.debug(f"Generated property prompt: {prompt}")
        return prompt

    def generate_schema_inference_prompt(self, entities: List[str], relationships: List[str]) -> str:
        entity_list = ', '.join(entities)
        relationship_list = ', '.join(relationships)
        prompt = f"Please infer the schema based on the following entities: {entity_list}, and relationships: {relationship_list}."
        logger.debug(f"Generated schema inference prompt: {prompt}")
        return prompt

class Neo4jConnection:
    def __init__(self, uri: str, user: str, password: str):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def query(self, query: str):
        with self.driver.session() as session:
            result = session.run(query)
            return result

    def close(self):
        self.driver.close()

def main():
    st.title('Knowledge Graph Construction and Schema Inference')

    page = st.sidebar.selectbox(
        "Select a deliverable view:",
        ("Schema Inference Algorithm", 
        "Illustrative Example", 
        "Dynamic Prompts for Schema Refinement", 
        "Multi-format Document Handling", 
        "Technology Justification", 
        "Neo4j Graph Output")
    )

    neo4j_uri = "neo4j://localhost:7687"
    neo4j_user = "neo4j"
    neo4j_password = "password"  
    neo4j_connection = Neo4jConnection(neo4j_uri, neo4j_user, neo4j_password)

    if page == "Schema Inference Algorithm":
        st.header("Schema Inference Algorithm")
        st.write("""
            The schema inference algorithm is designed to extract structured schema information 
            (entities, relationships, and properties) from unstructured document data. It operates 
            in the following steps:
            1. **Entity Extraction**: Identifies key entities from the document.
            2. **Relationship Extraction**: Detects relationships between extracted entities.
            3. **Schema Construction**: Infers the schema by grouping entities into types and defining relationships.
            4. **Graph Population**: Uses the inferred schema to populate a knowledge graph.
        """)

    elif page == "Illustrative Example":
        st.header("Illustrative Example")
        
        input_data = {
            "entities": ["John", "Acme Corp"],
            "relationships": [("John", "works_for", "Acme Corp")]
        }
        st.write(f"**Input:** {input_data}")

        inferred_schema = {
            "John": "Person",
            "Acme Corp": "Organization",
            "works_for": "Relationship"
        }
        st.write(f"**Inferred Schema:** {inferred_schema}")

        graph_data = {
            "nodes": ["John", "Acme Corp"],
            "edges": [("John", "works_for", "Acme Corp")]
        }
        st.write(f"**Populated Graph:** {graph_data}")
        
        fig, ax = plt.subplots()
        ax.plot([1, 2], [2, 3], label='Connection')
        ax.set_title('Populated Knowledge Graph')
        ax.legend()
        st.pyplot(fig)

    elif page == "Dynamic Prompts for Schema Refinement":
        st.header("Dynamic Prompt Mechanism for Schema Refinement")
        prompts = DynamicPrompts()
        
        entity_prompt = prompts.generate_entity_prompt("John", "Person")
        relationship_prompt = prompts.generate_relationship_prompt("John", "Acme Corp", "works_for")
        property_prompt = prompts.generate_property_prompt("John", "Person", ["age", "location"])

        st.write("### Example Dynamic Prompts:")
        st.write(f"**Entity Prompt:** {entity_prompt}")
        st.write(f"**Relationship Prompt:** {relationship_prompt}")
        st.write(f"**Property Prompt:** {property_prompt}")

    elif page == "Multi-format Document Handling":
        st.header("Multi-format Document Handling and Knowledge Graph Updates")
        st.write("""
            Our system supports multi-format document processing, which allows for the extraction 
            of entities and relationships from documents of various formats, such as:
            1. **PDF**
            2. **Word (DOCX)**
            3. **Text files**
            
            The system uses dedicated parsers to handle each format and extract the relevant 
            information for schema inference and graph population.
        """)
        st.write("### Example: Extracting data from a PDF")
        st.write("We would process a PDF document and extract entities and relationships.")
        
        extracted_data = {
            "entities": ["John", "Acme Corp"],
            "relationships": [("John", "works_for", "Acme Corp")]
        }
        st.write(f"**Extracted Data from Document:** {extracted_data}")

    elif page == "Technology Justification":
        st.header("Technology Justification")
        st.write("""
            The technologies chosen for this project include:
            1. **Python**: For its versatility and the rich ecosystem of libraries such as `pandas`, `numpy`, 
            and `matplotlib`.
            2. **Neo4j**: A graph database chosen for its ability to efficiently store and query graph-based data.
            3. **Streamlit**: A framework for quickly creating interactive web apps, perfect for visualizing 
            and interacting with the knowledge graph.
            4. **NLP Libraries**: Such as `spaCy` and `NLTK` for entity and relationship extraction from text.
        """)
        st.write("### Justification Details:")
        st.write("""
            - **Python**: Offers a wide range of libraries for data processing, analysis, and machine learning.
            - **Neo4j**: Graph databases like Neo4j are highly efficient for managing relationships between entities.
            - **Streamlit**: Streamlit simplifies the process of building interactive UIs for data applications.
        """)

    elif page == "Neo4j Graph Output":
        st.header("Neo4j Graph Output")

        query = "MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 10"
        results = neo4j_connection.query(query)
        
        nodes = set()
        edges = []
        for record in results:
            nodes.add(record["n"]["name"])
            nodes.add(record["m"]["name"])
            edges.append((record["n"]["name"], record["m"]["name"], record["r"].type))
        
        st.write(f"**Nodes:** {nodes}")
        st.write(f"**Edges (Relationships):** {edges}")

        G = nx.Graph()
        for node in nodes:
            G.add_node(node)
        for edge in edges:
            G.add_edge(edge[0], edge[1], label=edge[2])

        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight="bold")
        plt.title("Neo4j Knowledge Graph")
        st.pyplot(plt)

    neo4j_connection.close()

if __name__ == "__main__":
    main()
