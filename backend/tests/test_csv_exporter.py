import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Prueba de CSVExporter.
# Guarda dos claves, las exporta por versión y limpia.

from infrastructure.sqlite_repository import SQLiteRepository
from infrastructure.csv_exporter import CSVExporter
from domain.key import Key
from datetime import datetime
from config import ALGORITHM_VERSION

repo = SQLiteRepository()
repo.connect()

key1 = Key(value="abc123", timestamp=datetime.now(), algorithm_version=ALGORITHM_VERSION)
key2 = Key(value="def456", timestamp=datetime.now(), algorithm_version=ALGORITHM_VERSION)

repo.save_key(key1)
repo.save_key(key2)

keys = repo.get_keys_by_version(ALGORITHM_VERSION)

exporter = CSVExporter()
exporter.export_keys(keys, f"test_export_{ALGORITHM_VERSION}.csv")

repo.delete_keys_by_version(ALGORITHM_VERSION)
print("Base de datos limpia.")

repo.release()