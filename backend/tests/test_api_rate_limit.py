import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Verifica que el rate limiting de la API funciona correctamente.
# Requiere que el servidor esté corriendo en localhost:8000 (opción 5 del menú).

import time
import requests

BASE_URL = "http://localhost:8000"

print("Test rate limiting — /keys/generate (límite: 10/minuto)\n")

for i in range(12):
    response = requests.post(f"{BASE_URL}/keys/generate?cantidad=1&formato=json")
    print(f"  Petición {i+1}: HTTP {response.status_code}")
    if response.status_code == 429:
        print("  → Rate limit activado correctamente")
        break

print("\nTest rate limiting — /keys/send-email (límite: 5/minuto)\n")

for i in range(7):
    response = requests.post(f"{BASE_URL}/keys/send-email?cantidad=1&formato=txt&email=test@test.com")
    print(f"  Petición {i+1}: HTTP {response.status_code}")
    if response.status_code == 429:
        print("  → Rate limit activado correctamente")
        break