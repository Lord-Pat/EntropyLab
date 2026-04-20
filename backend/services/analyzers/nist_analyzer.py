import numpy as np
from scipy.stats import chi2
from scipy.special import erfc
from datetime import datetime
from domain.nist_result import NistResult
import uuid

class NistAnalyzer:

    def analizar(self, keys, version):
        bits = ""
        for k in keys:
            valor = k.value.replace("-", "")
            bits += bin(int(valor, 16))[2:].zfill(128)

        secuencia = np.array([int(b) for b in bits])
        n = len(secuencia)

        p_values = {}
        passed_tests = []

        # Test 1: Frecuencia monobit
        s = np.sum(secuencia * 2 - 1)
        p = float(erfc(abs(s) / np.sqrt(n) / np.sqrt(2)))
        p_values["monobit"] = round(p, 6)
        if p >= 0.01:
            passed_tests.append("monobit")

        # Test 2: Frecuencia por bloques
        M = 128
        num_bloques = n // M
        chi_sq = sum(
            (np.sum(secuencia[i*M:(i+1)*M]) / M - 0.5) ** 2
            for i in range(num_bloques)
        ) * 4 * M
        p = float(1 - chi2.cdf(chi_sq, num_bloques))
        p_values["frecuencia_bloques"] = round(p, 6)
        if p >= 0.01:
            passed_tests.append("frecuencia_bloques")

        # Test 3: Rachas
        pi = np.sum(secuencia) / n
        if abs(pi - 0.5) >= 2 / np.sqrt(n):
            p = 0.0
        else:
            rachas = 1 + np.sum(secuencia[:-1] != secuencia[1:])
            p = float(erfc(abs(rachas - 2*n*pi*(1-pi)) / (2*np.sqrt(2*n)*pi*(1-pi))))
        p_values["rachas"] = round(p, 6)
        if p >= 0.01:
            passed_tests.append("rachas")

        # Test 4: Entropía aproximada
        m = 10
        def phi(seq, longitud):
            total = len(seq) - longitud + 1
            patrones = {}
            for i in range(total):
                p = tuple(seq[i:i+longitud])
                patrones[p] = patrones.get(p, 0) + 1
            return sum((c/total) * np.log(c/total) for c in patrones.values() if c > 0)

        lista = list(secuencia)
        ap_en = phi(lista, m) - phi(lista, m+1)
        chi_sq = 2 * n * (np.log(2) - ap_en)
        p = float(1 - chi2.cdf(chi_sq, 2**m))
        p_values["entropia_aproximada"] = round(p, 6)
        if p >= 0.01:
            passed_tests.append("entropia_aproximada")

        print("\n" + "═" * 55)
        print("  NIST SP800-22")
        for nombre, pv in p_values.items():
            estado = "✓ PASS" if nombre in passed_tests else "✗ FAIL"
            print(f"  {estado}  |  {nombre:<25}  |  p={pv}")
        print("═" * 55)
        print(f"  {len(passed_tests)}/{len(p_values)} tests pasados\n")

        return NistResult(
            result_id=str(uuid.uuid4())[:8],
            timestamp=datetime.now(),
            algorithm_version=version,
            sample_size=len(keys),
            p_values=p_values,
            passed_tests=passed_tests,
            notes=f"{len(passed_tests)}/{len(p_values)} tests NIST pasados"
        )