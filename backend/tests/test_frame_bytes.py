# Mide los fps de la cámara

from infrastructure.camera_reader import CameraReader

camera = CameraReader()
camera.connect()
frame = camera.read_frame()
print(frame)
camera.release()