from neo4j import GraphDatabase
from config import Config
import logging
logger = logging.getLogger(__name__)

class GraphQuery:
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
            logger.info("Successfully connected to Neo4j database for querying")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j database: {e}")

    def close_connection(self):
        if self.driver:
            self.driver.close()
            logger.info("Closed the Neo4j connection for querying")

    def fetch_entities(self):
        try:
            with self.driver.session() as session:
                result = session.run("MATCH (e:Entity) RETURN e.name AS entity, e.type AS type")
                entities = [{"name": record["entity"], "type": record["type"]} for record in result]
                logger.info(f"Fetched {len(entities)} entities from the graph")
                return entities
        except Exception as e:
            logger.error(f"Failed to fetch entities from the graph: {e}")
            return []

    def fetch_relationships(self):
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (a:Entity)-[r:RELATED_TO]->(b:Entity)
                    RETURN a.name AS source, b.name AS target, r.type AS relation
                    """)
                relationships = [{"source": record["source"], "target": record["target"], "relation": record["relation"]} for record in result]
                logger.info(f"Fetched {len(relationships)} relationships from the graph")
                return relationships
        except Exception as e:
            logger.error(f"Failed to fetch relationships from the graph: {e}")
            return []