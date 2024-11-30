import json

class JSONParser:
    def parse(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return json.dumps(data, indent=2)