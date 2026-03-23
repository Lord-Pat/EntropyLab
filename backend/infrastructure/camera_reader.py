import cv2
from datetime import datetime
from domain.entropy_frame import EntropyFrame
from config import STREAM_URL

class CameraReader:
    
    def __init__(self):
        self.stream_url = STREAM_URL
        self.cap = None

    def connect(self):
        self.cap = cv2.VideoCapture(self.stream_url)
        if not self.cap.isOpened():
            raise ConnectionError("No se puede conectar al stream: " + self.stream_url)
        print("Conectado al stream: " + self.stream_url)

    def read_frame(self):
        if self.cap is None:
            raise RuntimeError("Cámara no conectada. Llama a connect() primero.")
        
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Error leyendo frame del stream.")
        
        return EntropyFrame(
            timestamp=datetime.now(),
            raw_bytes=frame.tobytes()
        )

    def release(self):
        if self.cap:
            self.cap.release()
            self.cap = None
            print("Cámara liberada.")