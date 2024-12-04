from neo4j import GraphDatabase
from config import Config
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class KnowledgeGraph:
    def __init__(self):
        self.config = Config()
        self.uri = self.config.NEO4J_URI
        self.username = self.config.NEO4J_USER
        self.password = self.config.NEO4J_PASSWORD
        self.driver = None
        self.connect_to_neo4j()

    def connect_to_neo4j(self):
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
            logger.info("Successfully connected to Neo4j database.")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j database: {e}")
            raise e

    def close_connection(self):
        if self.driver:
            self.driver.close()
            logger.info("Closed the Neo4j connection.")

    def create_entity(self, entity_name: str, entity_type: str = "Entity", properties: Dict = None):
        try:
            query = f"""
            MERGE (e:{entity_type} {{name: $name}})
            SET e += $properties
            """
            with self.driver.session() as session:
                session.run(query, name=entity_name, properties=properties or {})
            logger.info(f"Entity '{entity_name}' of type '{entity_type}' created/updated successfully.")
        except Exception as e:
            logger.error(f"Failed to create/update entity '{entity_name}': {e}")
            raise e

    def create_relationship(self, source: str, target: str, relation_type: str, properties: Optional[Dict] = None):
        try:
            query = f"""
            MATCH (a {{name: $source}})
            MATCH (b {{name: $target}})
            MERGE (a)-[r:{relation_type}]->(b)
            SET r += $properties
            """
            with self.driver.session() as session:
                session.run(query, source=source, target=target, properties=properties or {})
            logger.info(f"Relationship '{relation_type}' created/updated between '{source}' and '{target}' with properties: {properties}.")
        except Exception as e:
            logger.error(f"Failed to create/update relationship '{relation_type}' between '{source}' and '{target}': {e}")
            raise e

    def add_entities_and_relationships(self, entities: List[Dict], relationships: List[Dict]):
        try:
            with self.driver.session() as session:
                for entity in entities:
                    name = entity.get("name")
                    entity_type = entity.get("type", "Entity")
                    properties = entity.get("properties", {})
                    query = f"""
                    MERGE (n:{entity_type} {{name: $name}})
                    SET n += $properties
                    """
                    session.run(query, name=name, properties=properties)
                    logger.info(f"Added/Updated entity: {name} of type: {entity_type} with properties: {properties}.")

                for relationship in relationships:
                    source = relationship.get("source")
                    target = relationship.get("target")
                    rel_type = relationship.get("type", "RelatedTo")
                    properties = relationship.get("properties", {})
                    query = f"""
                    MATCH (a {{name: $source}})
                    MATCH (b {{name: $target}})
                    MERGE (a)-[r:{rel_type}]->(b)
                    SET r += $properties
                    """
                    session.run(query, source=source, target=target, properties=properties)
                    logger.info(f"Added/Updated relationship: {rel_type} between {source} and {target} with properties: {properties}.")
        except Exception as e:
            logger.error(f"Failed to add entities and relationships: {e}")
            raise e

    def query_graph(self, query: str, parameters: Optional[Dict] = None):
        try:
            with self.driver.session() as session:
                result = session.run(query, parameters or {})
                return [record.data() for record in result]
        except Exception as e:
            logger.error(f"Failed to execute query: {e}")
            raise e

    def get_nodes_and_relationships(self):
        try:
            query = "MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 25"
            with self.driver.session() as session:
                result = session.run(query)
                nodes = []
                relationships = []
                for record in result:
                    nodes.append(record["n"])
                    nodes.append(record["m"])
                    relationships.append(record["r"])
                logger.info(f"Retrieved nodes: {len(nodes)}, relationships: {len(relationships)}")
                return nodes, relationships
        except Exception as e:
            logger.error(f"Failed to retrieve nodes and relationships: {e}")
            raise e

    def delete_entity(self, entity_name: str):
        try:
            query = "MATCH (e {name: $name}) DETACH DELETE e"
            with self.driver.session() as session:
                result = session.run(query, name=entity_name)
                if result.consume().counters.nodes_deleted > 0:
                    logger.info(f"Entity '{entity_name}' deleted successfully.")
                else:
                    logger.warning(f"Entity '{entity_name}' does not exist.")
        except Exception as e:
            logger.error(f"Failed to delete entity '{entity_name}': {e}")
            raise e

    def update_entity_properties(self, entity_name: str, properties: Dict):
        try:
            query = """
            MATCH (e {name: $name})
            SET e += $properties
            RETURN e
            """
            with self.driver.session() as session:
                result = session.run(query, name=entity_name, properties=properties)
                updated_entity = result.single()
                if updated_entity:
                    logger.info(f"Updated entity '{entity_name}' with properties: {properties}.")
                else:
                    logger.warning(f"Entity '{entity_name}' not found.")
        except Exception as e:
            logger.error(f"Failed to update entity '{entity_name}': {e}")
            raise e