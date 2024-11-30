from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt
from config import Config
import logging
logger = logging.getLogger(__name__)

class GraphVisualization:
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
            logger.info("Successfully connected to Neo4j database for visualization")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j database: {e}")

    def close_connection(self):
        if self.driver:
            self.driver.close()
            logger.info("Closed the Neo4j connection for visualization")

    def visualize_graph(self):
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (a:Entity)-[r:RELATED_TO]->(b:Entity)
                    RETURN a.name AS source, b.name AS target, r.type AS relation
                    """)
                G = nx.Graph()
                for record in result:
                    G.add_edge(record["source"], record["target"], label=record["relation"])

                plt.figure(figsize=(10, 10))
                pos = nx.spring_layout(G)
                nx.draw_networkx_nodes(G, pos, node_size=700)
                nx.draw_networkx_labels(G, pos, font_size=10)
                nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
                labels = nx.get_edge_attributes(G, 'label')
                nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
                plt.title("Entity Relationship Graph")
                plt.show()
                logger.info("Graph visualization displayed successfully")
        except Exception as e:
            logger.error(f"Failed to visualize the graph: {e}")