import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Prueba de KeyGeneratorService.
# Genera tres GUIDs usando entropía física de la ESP32,
# los guarda en SQLite y verifica que se recuperan correctamente.
# Uso: verificar que el generador produce GUIDs distintos y bien formateados.
# AVISO: este test borra todas las claves de la BD al finalizar. No ejecutar con datos de producción.

from infrastructure.camera_reader import CameraReader
from infrastructure.sqlite_repository import SQLiteRepository
from services.entropy_service import EntropyService
from services.key_generator_service import KeyGeneratorService

camera = CameraReader()
camera.connect()

repo = SQLiteRepository()
repo.connect()

entropy_svc = EntropyService(camera)
key_svc = KeyGeneratorService(entropy_svc, repo)

print("--- Generando GUIDs ---")
key1 = key_svc.generate()
key2 = key_svc.generate()
key3 = key_svc.generate()

print(f"GUID 1: {key1.value}")
print(f"GUID 2: {key2.value}")
print(f"GUID 3: {key3.value}")
print(f"Son distintos: {key1.value != key2.value != key3.value}")

print("\n--- Claves en base de datos ---")
keys = repo.get_all_keys()
print(f"Total guardadas: {len(keys)}")

for k in keys:
    print(f"  [ID {k.key_id}] {k.value}")

repo.clear_keys()
print("Base de datos limpia.")

camera.release()
repo.release()