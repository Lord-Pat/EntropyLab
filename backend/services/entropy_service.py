import hashlib
import numpy as np
from infrastructure.camera_reader import CameraReader

class EntropyService:

    def __init__(self, camera_reader):
        self.camera_reader = camera_reader
        self.previous_frame = None

    def extract_entropy(self):
        if self.previous_frame is None:
            frame1 = self.camera_reader.read_frame()
        else:
            frame1 = self.previous_frame
        
        frame2 = self.camera_reader.read_frame()
        self.previous_frame = frame2

        bytes1 = np.frombuffer(frame1.raw_bytes, dtype=np.uint8)
        bytes2 = np.frombuffer(frame2.raw_bytes, dtype=np.uint8)

        diferencia = np.abs(bytes1.astype(np.int16) - bytes2.astype(np.int16)).astype(np.uint8)

        entropia = hashlib.sha256(diferencia.tobytes()).digest()

        # importante! hashlib.sha256 devuelve 32 bits, pero solo usaremos 16. Esto está pensado para poder usar en el futuro hashes más completos,
        # y es como funciona esta librería en concreto.

        return entropia

