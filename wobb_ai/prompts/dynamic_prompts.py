class DynamicPrompts:
    def refine_schema(self, schema):
        print("Current Schema:", schema)
        user_input = input("Enter additional entities or relationships (comma-separated): ")
        additions = user_input.split(",")
        for addition in additions:
            if "->" in addition:
                start, end = addition.split("->")
                schema["relationships"].append((start.strip(), "related_to", end.strip()))
            else:
                schema["entities"].append(addition.strip())
        return schema