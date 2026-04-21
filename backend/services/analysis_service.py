from services.analyzers.nist_analyzer import NistAnalyzer
from services.analyzers.shannon_analyzer import ShannonAnalyzer
from services.analyzers.autocorrelation_analyzer import AutocorrelationAnalyzer
from services.analyzers.maurer_analyzer import MaurerAnalyzer

class AnalysisService:

    def __init__(self, repository):
        self.repository = repository
        self.nist = NistAnalyzer()
        self.shannon = ShannonAnalyzer()
        self.autocorrelation = AutocorrelationAnalyzer()
        self.maurer = MaurerAnalyzer()

    def analizar(self, version):
        keys = self.repository.get_keys_by_version(version)
        if len(keys) < 1000:
            print(f"Muestra insuficiente: {len(keys)} claves. Se recomiendan al menos 1000.")
            return

        print(f"Analizando {len(keys)} claves de versión {version}...")

        nist_result = self.nist.analizar(keys, version)
        self.repository.save_nist_result(nist_result)
        print("Resultado NIST guardado.")

        shannon_result = self.shannon.analizar(keys, version)
        self.repository.save_shannon_result(shannon_result)
        print("Resultado Shannon guardado.")

        autocorr_result = self.autocorrelation.analizar(keys, version)
        self.repository.save_autocorrelation_result(autocorr_result)
        print("Resultado Autocorrelación guardado.")

        maurer_result = self.maurer.analizar(keys, version)
        self.repository.save_maurer_result(maurer_result)
        print("Resultado Maurer guardado.")