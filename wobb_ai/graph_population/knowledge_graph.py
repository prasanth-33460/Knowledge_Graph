import json
from neo4j import GraphDatabase
from config import Config
import logging
import json
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class KnowledgeGraph:
    def __init__(self,):
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

    def create_entity(self, entity_name: str, entity_type: str, properties: Dict = None):
        try:
            query = f"""
            MERGE (e:{entity_type} {{name: $name}})
            SET e += $properties
            """
            with self.driver.session() as session:
                session.run(query, name=entity_name, properties=properties or {})
            logger.info(f"Entity '{entity_name}' of type '{entity_type}' created successfully.")
        except Exception as e:
            logger.error(f"Failed to create entity '{entity_name}': {e}")
            raise e

    def create_relationship(self, source: str, target: str, relation_type: str, properties: Optional[Dict] = None):
        try:
            with self.driver.session() as session:
                query = """
                    MATCH (a:Entity {name: $source}), (b:Entity {name: $target})
                    MERGE (a)-[r:RELATED_TO {type: $relation_type}]->(b)
                    SET r.properties = $properties
                """
                session.run(query, source=source, target=target, relation_type=relation_type, properties=properties or {})
                logger.info(f"Relationship '{relation_type}' created/merged between '{source}' and '{target}' with properties: {properties}")
        except Exception as e:
            logger.error(f"Failed to create relationship '{relation_type}' between '{source}' and '{target}': {e}")
            raise e

    def find_entities(self, entity_name: Optional[str] = None, entity_type: Optional[str] = None) -> List[Dict]:
        try:
            with self.driver.session() as session:
                query = """
                    MATCH (e:Entity)
                    WHERE ($name IS NULL OR e.name = $name)
                    AND ($type IS NULL OR e.type = $type)
                    RETURN e
                """
                result = session.run(query, name=entity_name, type=entity_type)
                entities = [{"name": record["e"]["name"], "type": record["e"]["type"], "properties": record["e"]["properties"]} for record in result]
                logger.info(f"Retrieved entities: {entities}")
                return entities
        except Exception as e:
            logger.error(f"Failed to find entities: {e}")
            raise e
        
    def add_entities_and_relationships(self, entities, relationships):
        if not self.driver:
            logger.error("Neo4j connection not initialized!")
            return        
        try:
            with self.driver.session() as session:
                for entity in entities:
                    if isinstance(entity, dict):
                        name = entity.get("name")
                        type_ = entity.get("type")
                        session.run("CREATE (n:Entity {name: $name, type: $type})", name=name, type=type_)
                    else:
                        session.run("CREATE (n:Entity {name: $name})", name=entity)
                for relationship in relationships:
                    source = relationship.get('source')
                    target = relationship.get('target')
                    rel_type = relationship.get('type')
                    if source and target and rel_type:
                        session.run(
                            "MATCH (a:Entity {name: $source}), (b:Entity {name: $target}) "
                            "CREATE (a)-[:RELATIONSHIP {type: $type}]->(b)",
                            source=source, target=target, type=rel_type
                        )
                    else:
                        logger.warning(f"Missing required keys in relationship: {relationship}")
        except Exception as e:
            logger.error(f"Error occurred while adding entities and relationships: {e}")

    def find_relationships(self, source: Optional[str] = None, target: Optional[str] = None, relation_type: Optional[str] = None) -> List[Dict]:
        try:
            with self.driver.session() as session:
                query = """
                    MATCH (a:Entity)-[r:RELATED_TO]->(b:Entity)
                    WHERE ($source IS NULL OR a.name = $source)
                    AND ($target IS NULL OR b.name = $target)
                    AND ($type IS NULL OR r.type = $type)
                    RETURN a.name AS source, b.name AS target, r.type AS relation_type, r.properties AS relation_properties
                """
                result = session.run(query, source=source, target=target, type=relation_type)
                relationships = [
                    {
                        "source": record["source"],
                        "target": record["target"],
                        "relation_type": record["relation_type"],
                        "relation_properties": record["relation_properties"],
                    }
                    for record in result
                ]
                logger.info(f"Retrieved relationships: {relationships}")
                return relationships
        except Exception as e:
            logger.error(f"Failed to find relationships: {e}")
            raise e

    def delete_entity(self, entity_name: str):
        try:
            with self.driver.session() as session:
                query = """
                    MATCH (e:Entity {name: $name})
                    DETACH DELETE e
                """
                session.run(query, name=entity_name)
                logger.info(f"Entity '{entity_name}' deleted successfully.")
        except Exception as e:
            logger.error(f"Failed to delete entity '{entity_name}': {e}")
            raise e

    def update_entity_properties(self, entity_name: str, properties: Dict):
        try:
            with self.driver.session() as session:
                query = """
                    MATCH (e:Entity {name: $name})
                    SET e.properties = $properties
                    RETURN e
                """
                result = session.run(query, name=entity_name, properties=properties)
                if result.single():
                    logger.info(f"Entity '{entity_name}' updated with properties: {properties}")
                else:
                    logger.warning(f"Entity '{entity_name}' not found.")
        except Exception as e:
            logger.error(f"Failed to update entity '{entity_name}': {e}")
            raise e