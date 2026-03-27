# Prueba de la clase CSVExporter de infraestructura.
# Guarda dos claves de prueba, las exporta a CSV y limpia la base de datos.
# Uso: verificar que el exportador crea la carpeta exports/ y escribe el fichero correctamente.


import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

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

keys = repo.get_all_keys()

exporter = CSVExporter()
exporter.export_keys(keys, "test_export.csv")

repo.clear_keys()
repo.release()