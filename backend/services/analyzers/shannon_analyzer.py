import math
from datetime import datetime
from domain.shannon_result import ShannonResult
import uuid

class ShannonAnalyzer:

    def analizar(self, keys, version):
        todos_bytes = []
        for k in keys:
            valor = k.value.replace("-", "")
            todos_bytes.extend(bytes.fromhex(valor))

        total = len(todos_bytes)
        frecuencias = {}
        for b in todos_bytes:
            frecuencias[b] = frecuencias.get(b, 0) + 1

        entropia = 0.0
        for count in frecuencias.values():
            p = count / total
            entropia -= p * math.log2(p)

        entropia = round(entropia, 6)

        print(f"  Entropía de Shannon: {entropia} / 8.0 bits")
        print(f"  Eficiencia: {round(entropia/8.0*100, 2)}%\n")

        return ShannonResult(
            result_id=str(uuid.uuid4())[:8],
            timestamp=datetime.now(),
            algorithm_version=version,
            sample_size=len(keys),
            shannon=entropia,
            notes=f"Shannon: {entropia}/8.0 bits ({round(entropia/8.0*100, 2)}% eficiencia)"
        )