class ConflictResolution:
    def resolve(self, schema, new_schema):
        resolved_schema = schema.copy()
        for entity in new_schema["entities"]:
            if entity not in resolved_schema["entities"]:
                resolved_schema["entities"].append(entity)
        for relationship in new_schema["relationships"]:
            if relationship not in resolved_schema["relationships"]:
                resolved_schema["relationships"].append(relationship)
        return resolved_schema