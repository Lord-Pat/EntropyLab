# services/algorithms/v0_2_0.py
# copia del algoritmo anterior, PERO CON LA NUEVA LÁMPARA DE LAVA5

import hashlib
import numpy as np

def extraer_entropia(frame1, frame2):
    bytes1 = np.frombuffer(frame1.raw_bytes, dtype=np.uint8)
    bytes2 = np.frombuffer(frame2.raw_bytes, dtype=np.uint8)
    diferencia = np.abs(bytes1.astype(np.int16) - bytes2.astype(np.int16)).astype(np.uint8)
    return hashlib.sha256(diferencia.tobytes()).digest()