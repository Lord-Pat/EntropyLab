import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Lee un frame de la cámara y muestra sus propiedades

from infrastructure.camera_reader import CameraReader

camera = CameraReader()
camera.connect()
frame = camera.read_frame()
print(f"Timestamp: {frame.timestamp}")
print(f"Tamaño raw_bytes: {len(frame.raw_bytes)} bytes")
camera.release()