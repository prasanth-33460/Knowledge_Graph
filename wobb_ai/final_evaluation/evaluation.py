import networkx as nx
from typing import List, Dict
import logging
from final_evaluation.metrics import MetricsEvaluator

logger = logging.getLogger(__name__)

class GraphEvaluation:
    def __init__(self):
        self.metrics_evaluator = MetricsEvaluator()

    def evaluate(self, true_graph_data: List[Dict], predicted_graph_data: List[Dict]) -> Dict:
        try:
            logger.info("Starting evaluation process for the graph population...")

            if not true_graph_data or not predicted_graph_data:
                logger.error("No data provided for evaluation.")
                return {}

            logger.debug(f"True Graph Data: {true_graph_data}")
            logger.debug(f"Predicted Graph Data: {predicted_graph_data}")

            true_graphs = [self._build_graph(graph_data) for graph_data in true_graph_data]
            predicted_graphs = [self._build_graph(graph_data) for graph_data in predicted_graph_data]
            graph_metrics = self._evaluate_graphs(true_graphs, predicted_graphs)

            evaluation_results = self.metrics_evaluator.evaluate_graph_population(true_graph_data, predicted_graph_data)
            graph_metrics.update(evaluation_results)

            logger.info("Evaluation completed successfully.")
            return graph_metrics

        except Exception as e:
            logger.error(f"Error occurred during evaluation: {e}")
            return {}

    def _build_graph(self, graph_data: Dict) -> nx.Graph:
        logger.debug(f"Building graph from data: {graph_data}")
        graph = nx.Graph()
        nodes = graph_data.get("nodes", [])
        edges = graph_data.get("edges", [])
        
        if not nodes or not edges:
            logger.warning(f"Empty graph data: {graph_data}")

        graph.add_nodes_from(nodes)
        graph.add_edges_from(edges)
        return graph

    def _evaluate_graphs(self, true_graphs: List[nx.Graph], predicted_graphs: List[nx.Graph]) -> Dict:
        results = {}

        for idx, (true_graph, predicted_graph) in enumerate(zip(true_graphs, predicted_graphs)):
            logger.debug(f"Evaluating Graph_{idx}: {true_graph.nodes()} vs {predicted_graph.nodes()}")

            edit_distance = nx.graph_edit_distance(true_graph, predicted_graph)
            true_degree_centrality = nx.degree_centrality(true_graph)
            predicted_degree_centrality = nx.degree_centrality(predicted_graph)

            centrality_diff = sum(
                abs(true_degree_centrality[node] - predicted_degree_centrality.get(node, 0))
                for node in true_degree_centrality
            )

            results[f"Graph_{idx}"] = {
                "edit_distance": edit_distance,
                "centrality_difference": centrality_diff,
            }

        logger.debug(f"Graph evaluation results: {results}")
        return results