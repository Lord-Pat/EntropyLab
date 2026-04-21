import numpy as np
from scipy.special import erfc
from datetime import datetime
from domain.autocorrelation_result import AutocorrelationResult
import uuid

class AutocorrelationAnalyzer:

    def _test_lag(self, secuencia, lag):
        n = len(secuencia)
        correlacion = np.sum(secuencia[:n-lag] == secuencia[lag:]) / (n - lag)
        z = (correlacion - 0.5) / np.sqrt(0.25 / (n - lag))
        p = float(erfc(abs(z) / np.sqrt(2)))
        return float(correlacion), p

    def analizar(self, keys, version):
        bits = ""
        for k in keys:
            valor = k.value.replace("-", "")
            bits += bin(int(valor, 16))[2:].zfill(128)

        secuencia = np.array([int(b) for b in bits])

        lag1_corr, lag1_p = self._test_lag(secuencia, 1)
        lag8_corr, lag8_p = self._test_lag(secuencia, 8)

        print("\n  Autocorrelación serial")
        print(f"  {'✓ PASS' if lag1_p >= 0.01 else '✗ FAIL'}  |  lag=1  |  corr={lag1_corr:.6f}  p={lag1_p:.6f}")
        print(f"  {'✓ PASS' if lag8_p >= 0.01 else '✗ FAIL'}  |  lag=8  |  corr={lag8_corr:.6f}  p={lag8_p:.6f}")

        estado_lag1 = "PASS" if lag1_p >= 0.01 else "FAIL"
        estado_lag8 = "PASS" if lag8_p >= 0.01 else "FAIL"

        return AutocorrelationResult(
            result_id=str(uuid.uuid4())[:8],
            timestamp=datetime.now(),
            algorithm_version=version,
            sample_size=len(keys),
            lag1_correlation=lag1_corr,
            lag1_p=lag1_p,
            lag8_correlation=lag8_corr,
            lag8_p=lag8_p,
            notes=f"lag1: {estado_lag1} (p={lag1_p:.6f}) | lag8: {estado_lag8} (p={lag8_p:.6f})"
        )