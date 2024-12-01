from typing import List, Dict
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import logging

logger = logging.getLogger(__name__)

class MetricsEvaluator:
    def __init__(self):
        pass

    def calculate_metrics(self, true_values: List[Dict], predicted_values: List[Dict]) -> Dict:
        try:
            if not true_values or not predicted_values:
                logger.warning("No values to compare for metrics calculation.")
                return {}

            logger.debug(f"True Values: {true_values}")
            logger.debug(f"Predicted Values: {predicted_values}")

            true_labels = [item['label'] for item in true_values if 'label' in item]
            predicted_labels = [item['label'] for item in predicted_values if 'label' in item]

            if not true_labels or not predicted_labels:
                logger.warning("No valid labels found in the data.")
                return {}

            accuracy = accuracy_score(true_labels, predicted_labels)
            precision = precision_score(true_labels, predicted_labels, average='weighted', zero_division=0)
            recall = recall_score(true_labels, predicted_labels, average='weighted', zero_division=0)
            f1 = f1_score(true_labels, predicted_labels, average='weighted', zero_division=0)

            logger.info(f"Accuracy: {accuracy}")
            logger.info(f"Precision: {precision}")
            logger.info(f"Recall: {recall}")
            logger.info(f"F1-Score: {f1}")
            return {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1
            }
        except Exception as e:
            logger.error(f"Error occurred during metrics calculation: {e}")
            return {}

    def evaluate_graph_population(self, true_graph_data: List[Dict], predicted_graph_data: List[Dict]) -> Dict:
        logger.info("Evaluating graph population performance...")

        if not true_graph_data or not predicted_graph_data:
            logger.error("Missing true or predicted graph data.")
            return {}

        return self.calculate_metrics(true_graph_data, predicted_graph_data)