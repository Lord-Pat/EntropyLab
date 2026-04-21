import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Prueba de la clase EntropyService de servicios.
# Extrae dos muestras de entropía usando el algoritmo activo en config.py.
# El número de frames capturados depende del algoritmo (2 o 3 según algorithms.json).
# Uso: verificar que el servicio extrae entropía y que cada ejecución produce un resultado diferente (no determinista).

from infrastructure.camera_reader import CameraReader
from services.entropy_service import EntropyService

camera = CameraReader()
camera.connect()

entropy_svc = EntropyService(camera)

entropia1 = entropy_svc.extract_entropy()
entropia2 = entropy_svc.extract_entropy()

print(f"Bytes de entropía: {len(entropia1)}")
print(f"Resultado 1: {entropia1.hex()}")
print(f"Resultado 2: {entropia2.hex()}")
print(f"Son distintos: {entropia1 != entropia2}")

camera.release()