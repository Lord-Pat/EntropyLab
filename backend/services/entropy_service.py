import hashlib
import numpy as np
from infrastructure.camera_reader import CameraReader
from domain.entropy_frame import EntropyFrame

class EntropyService:

    def __init__(self, camera_reader):
        self.camera_reader = camera_reader

    def extract_entropy(self):
        frame1 = self.camera_reader.read_frame()
        frame2 = self.camera_reader.read_frame()

        bytes1 = np.frombuffer(frame1.raw_bytes, dtype=np.uint8)
        bytes2 = np.frombuffer(frame2.raw_bytes, dtype=np.uint8)

        diferencia = np.abs(bytes1.astype(np.int16) - bytes2.astype(np.int16)).astype(np.uint8)

        entropia = hashlib.sha256(diferencia.tobytes()).digest()

        return entropia

