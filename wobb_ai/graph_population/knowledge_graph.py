import networkx as nx

class KnowledgeGraph:
    def __init__(self):
        self.Graph = nx.Graph()
        
    def build_graph(self, entities, relationships):
        for entity in entities:
            self.Graph.add_node(entity['text'], label = entity['label'])
        for relationship in relationships:
            self.Graph.add_edge(relationship['entity1'], relationship['entity2'], relationship=relationship['relationship'])
            
    def display_graph(self):
        nx.draw(self.Graph, with_labels=True,font_weight='bold')
        
    def update_graph(self, new_entities, new_relationships):
        for entity in new_entities:
            if entity['text'] not in self.Graph.nodes:
                self.Graph.add_node(entity['text'],label=entity['label'])
        for relationships in new_relationships:
            if not self.Graph.has_edge(relationships['entity1'],relationships['entity2']):
                self.Graph.add_edge(relationships['entity1'], relationships['entity2'], relationship=relationships['relationship'])