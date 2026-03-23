import csv
import os
from config import CSV_EXPORT_PATH

class CSVExporter:

    def __init__(self):
        self.export_path = CSV_EXPORT_PATH
        os.makedirs(self.export_path, exist_ok=True)

    def export_keys(self, keys, filename):
        filepath = os.path.join(self.export_path, filename)
        with open(filepath, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["key_id", "value", "timestamp", "algorithm_version"])
            for key in keys:
                writer.writerow([
                    key.key_id,
                    key.value,
                    key.timestamp.isoformat(),
                    key.algorithm_version
                ])
        print("Exportado: " + filepath)