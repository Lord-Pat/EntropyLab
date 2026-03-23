# Monitor continuo de disponibilidad de la ESP32.
# Comprueba cada 30 segundos que el puerto 80 responde.
# Uso: dejar corriendo en segundo plano para detectar desconexiones.


import socket
import time
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config import STREAM_URL

ESP32_IP = STREAM_URL.split("//")[1].split("/")[0]
ESP32_PORT = 80

while True:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        resultado = sock.connect_ex((ESP32_IP, ESP32_PORT))
        sock.close()
        if resultado == 0:
            print(f"[OK] ESP32 activa — {time.strftime('%H:%M:%S')}")
        else:
            print(f"[ERROR] Puerto cerrado — {time.strftime('%H:%M:%S')}")
    except Exception as e:
        print(f"[ERROR] — {time.strftime('%H:%M:%S')} — {e}")
    
    time.sleep(30)