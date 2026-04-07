import csv
import os
from config import CSV_EXPORT_PATH

class CSVExporter:

    def export_keys(self, keys, filename):
        os.makedirs(CSV_EXPORT_PATH, exist_ok=True)
        filepath = os.path.join(CSV_EXPORT_PATH, filename)
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["key_id", "value", "timestamp", "algorithm_version"])
            for key in keys:
                writer.writerow([
                    key.key_id,
                    key.value,
                    key.timestamp.isoformat(),
                    key.algorithm_version
                ])
        print(f"Exportadas {len(keys)} claves → {filepath}")