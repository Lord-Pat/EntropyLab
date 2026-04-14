import hashlib
import numpy as np

def extraer_entropia(frame1, frame2):
    bytes1 = np.frombuffer(frame1.raw_bytes, dtype=np.uint8)
    bytes2 = np.frombuffer(frame2.raw_bytes, dtype=np.uint8)

    diferencia = np.abs(bytes1.astype(np.int16) - bytes2.astype(np.int16)).astype(np.uint8)

    # Seleccionamos solo los píxeles con mayor movimiento
    # — los que superan el percentil 75 de diferencia
    umbral = np.percentile(diferencia, 75)
    zonas_activas = diferencia[diferencia >= umbral]

    return hashlib.sha256(zonas_activas.tobytes()).digest()