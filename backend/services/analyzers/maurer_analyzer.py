import math
from scipy.special import erfc
from datetime import datetime
from domain.maurer_result import MaurerResult
import uuid

class MaurerAnalyzer:

    def analizar(self, keys, version):
        bits = ""
        for k in keys:
            valor = k.value.replace("-", "")
            bits += bin(int(valor, 16))[2:].zfill(128)

        L = 7
        Q = 1280
        n = len(bits)
        K = n // L - Q

        tabla = {}
        for i in range(Q):
            bloque = bits[i*L:(i+1)*L]
            tabla[bloque] = i + 1

        suma = 0.0
        for i in range(Q, Q + K):
            bloque = bits[i*L:(i+1)*L]
            if bloque in tabla:
                distancia = i + 1 - tabla[bloque]
                if distancia > 0:
                    suma += math.log2(distancia)
            tabla[bloque] = i + 1

        fn = suma / K
        esperado = 6.196359
        varianza = 3.125
        c = 0.7 - 0.8/L + (4 + 32/L) * (K**(-3/L)) / 15
        sigma = c * math.sqrt(varianza / K)
        z = (fn - esperado) / sigma
        p = float(erfc(abs(z) / math.sqrt(2)))

        estado = "PASS" if p >= 0.01 else "FAIL"
        print(f"\n  Maurer's Universal Test")
        print(f"  {'✓ PASS' if p >= 0.01 else '✗ FAIL'}  |  fn={fn:.6f}  |  p={p:.6f}")

        return MaurerResult(
            result_id=str(uuid.uuid4())[:8],
            timestamp=datetime.now(),
            algorithm_version=version,
            sample_size=len(keys),
            fn=fn,
            p_value=p,
            notes=f"Maurer: {estado} (fn={fn:.6f}, p={p:.6f})"
        )