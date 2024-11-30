from neo4j import GraphDatabase
from config import Config

class GraphQuery:
    def __init__(self):
        self.driver = GraphDatabase.driver(Config.NEO4J_URI, auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD))

    def execute_query(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            return [record for record in result]