import hashlib
import numpy as np

def extraer_entropia(frame1, frame2, frame3):
    bytes1 = np.frombuffer(frame1.raw_bytes, dtype=np.uint8)
    bytes2 = np.frombuffer(frame2.raw_bytes, dtype=np.uint8)
    bytes3 = np.frombuffer(frame3.raw_bytes, dtype=np.uint8)

    diff_ab = np.abs(bytes1.astype(np.int16) - bytes2.astype(np.int16)).astype(np.uint8)
    diff_bc = np.abs(bytes2.astype(np.int16) - bytes3.astype(np.int16)).astype(np.uint8)

    combinado = np.bitwise_xor(diff_ab, diff_bc)

    return hashlib.sha256(combinado.tobytes()).digest()