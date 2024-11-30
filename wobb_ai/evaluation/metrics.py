class Metrics:
    def evaluate(self, schema, entities, relationships):
        completeness = len(entities) / len(schema["entities"])
        accuracy = len(relationships) / len(schema["relationships"])
        return {"completeness": completeness, "accuracy": accuracy}