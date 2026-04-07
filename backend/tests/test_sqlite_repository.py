import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Prueba de SQLiteRepository.
# Guarda una clave, la recupera, verifica los métodos nuevos por versión y limpia.

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
print(f"Total en BD: {len(keys)}")
for k in keys:
    print(f"  [ID {k.key_id}] {k.value} ({k.algorithm_version})")

count = repo.count_keys_by_version(ALGORITHM_VERSION)
print(f"Claves de versión {ALGORITHM_VERSION}: {count}")

repo.delete_keys_by_version(ALGORITHM_VERSION)
print("Claves de esa versión eliminadas.")

repo.release()