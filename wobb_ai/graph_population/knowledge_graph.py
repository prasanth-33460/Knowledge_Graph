from neo4j import GraphDatabase
from config import Config

class KnowledgeGraph:
    def __init__(self):
        self.driver = GraphDatabase.driver(Config.NEO4J_URI, auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD))

    def populate(self, schema, entities, relationships):
        with self.driver.session() as session:
            for entity in schema["entities"]:
                session.run("MERGE (e:Entity {name: $name})", name=entity)
            for rel in relationships:
                session.run("""
                    MATCH (e1:Entity {name: $start}), (e2:Entity {name: $end})
                    MERGE (e1)-[:RELATIONSHIP {type: $type}]->(e2)
                """, start=rel[0], end=rel[2], type=rel[1])