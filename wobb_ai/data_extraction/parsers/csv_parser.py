import csv

class CSVParser:
    def parse(self, file_path):
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            return "\n".join([", ".join(row) for row in reader])