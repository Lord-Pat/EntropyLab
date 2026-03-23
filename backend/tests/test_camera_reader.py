# Prueba de la clase CameraReader de infraestructura.
# Captura 30 frames a través de CameraReader y mide FPS.
# Uso: verificar que CameraReader conecta, lee frames y libera correctamente.


import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from infrastructure.camera_reader import CameraReader
import time

camera = CameraReader()
camera.connect()

frame_count = 0
start_time = time.time()

while frame_count < 30:
    frame = camera.read_frame()
    frame_count += 1
    elapsed = time.time() - start_time
    print(f"Frame {frame_count} | FPS: {frame_count/elapsed:.2f}")

camera.release()