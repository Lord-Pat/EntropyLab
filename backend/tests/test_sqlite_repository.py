# Prueba de la clase SQLiteRepository de infraestructura.
# Guarda una clave de prueba, la recupera y limpia la base de datos.
# Uso: verificar que el repositorio escribe y lee correctamente.


import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from infrastructure.sqlite_repository import SQLiteRepository
from domain.key import Key
from datetime import datetime
from config import ALGORITHM_VERSION

repo = SQLiteRepository()
repo.connect()

key = Key(
    value="abc123",
    timestamp=datetime.now(),
    algorithm_version=ALGORITHM_VERSION
)

repo.save_key(key)
print("Clave guardada")

keys = repo.get_all_keys()
print("Claves en la base de datos:", len(keys))
print(keys[0])

repo.clear_keys()
print("Base de datos limpia")

repo.release()