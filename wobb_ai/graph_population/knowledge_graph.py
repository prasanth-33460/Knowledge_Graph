from neo4j import GraphDatabase
from config import Config
import logging
logger = logging.getLogger(__name__)
class KnowledgeGraph:
    def __init__(self):
        self.config = Config() 
        self.uri = self.config.NEO4J_URI
        self.username = self.config.NEO4J_USERNAME
        self.password = self.config.NEO4J_PASSWORD
        self.driver = None
        self.connect_to_neo4j()

    def connect_to_neo4j(self):
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
            logger.info("Successfully connected to Neo4j database")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j database: {e}")

    def close_connection(self):
        if self.driver:
            self.driver.close()
            logger.info("Closed the Neo4j connection")

    def create_entity(self, entity_name, entity_type):
        try:
            with self.driver.session() as session:
                session.run("CREATE (e:Entity {name: $name, type: $type})", name=entity_name, type=entity_type)
                logger.info(f"Entity {entity_name} of type {entity_type} created successfully")
        except Exception as e:
            logger.error(f"Failed to create entity {entity_name}: {e}")

    def create_relationship(self, source, target, relation_type):
        try:
            with self.driver.session() as session:
                session.run("""
                    MATCH (a:Entity {name: $source}), (b:Entity {name: $target})
                    CREATE (a)-[r:RELATED_TO {type: $relation_type}]->(b)
                    """, source=source, target=target, relation_type=relation_type)
                logger.info(f"Created relationship {relation_type} between {source} and {target}")
        except Exception as e:
            logger.error(f"Failed to create relationship between {source} and {target}: {e}")