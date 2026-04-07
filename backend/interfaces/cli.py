import threading
from config import ALGORITHM_VERSION
from infrastructure.csv_exporter import CSVExporter

class CLI:

    def __init__(self, key_svc, repo, camera):
        self.key_svc = key_svc
        self.repo = repo
        self.camera = camera
        self._generando = False
        self._hilo = None

    def run(self):
        print("Sistema listo.")
        while True:
            opcion = self._menu()
            if opcion == "1":
                self._iniciar_generacion()
            elif opcion == "2":
                self._parar_generacion()
            elif opcion == "3":
                self._exportar_csv()
            elif opcion == "4":
                self._registrar_analisis()
            elif opcion == "5":
                self._api()
            elif opcion == "6":
                self._estado()
            elif opcion == "0":
                self._salir()
                break
            else:
                print("Opción no válida.")

    def _menu(self):
        gen_estado = "EN CURSO" if self._generando else "parada"
        print(f"\n╔══════════════════════════════════╗")
        print(f"║      EntropyLab v0.1             ║")
        print(f"╠══════════════════════════════════╣")
        print(f"║  1. Iniciar generación masiva    ║")
        print(f"║  2. Parar generación  [{gen_estado}]  ║" if self._generando else
              f"║  2. Parar generación             ║")
        print(f"║  3. Exportar a CSV               ║")
        print(f"║  4. Registrar análisis           ║")
        print(f"║  5. Arrancar servidor API        ║")
        print(f"║  6. Estado del sistema           ║")
        print(f"║  0. Salir                        ║")
        print(f"╚══════════════════════════════════╝")
        return input("Selecciona una opción: ").strip()

    def _iniciar_generacion(self):
        if self._generando:
            print("La generación ya está en curso.")
            return
        self._generando = True
        self._hilo = threading.Thread(target=self._bucle_generacion, daemon=True)
        self._hilo.start()
        print(f"Generación masiva iniciada (versión {ALGORITHM_VERSION}). Vuelve al menú para pararla.")

    def _bucle_generacion(self):
        contador = 0
        while self._generando:
            try:
                key = self.key_svc.generate()
                contador += 1
                if contador % 10 == 0:
                    print(f"  [{contador} claves generadas] última: {key.value}")
            except Exception as e:
                print(f"Error generando clave: {e}")

    def _parar_generacion(self):
        if not self._generando:
            print("La generación no está en curso.")
            return
        self._generando = False
        self._hilo.join(timeout=5)
        total = self.repo.count_keys_by_version(ALGORITHM_VERSION)
        print(f"Generación parada. Claves acumuladas de versión {ALGORITHM_VERSION}: {total}")

    def _exportar_csv(self):
        total = self.repo.count_keys_by_version(ALGORITHM_VERSION)
        if total == 0:
            print(f"No hay claves de versión {ALGORITHM_VERSION} para exportar.")
            return
        print(f"Hay {total} claves de versión {ALGORITHM_VERSION} para exportar.")
        filename = f"claves_{ALGORITHM_VERSION}.csv"
        keys = self.repo.get_keys_by_version(ALGORITHM_VERSION)
        exporter = CSVExporter()
        exporter.export_keys(keys, filename)
        confirmacion = input("¿Borrar estas claves de la BD? (s/n): ").strip().lower()
        if confirmacion == "s":
            self.repo.delete_keys_by_version(ALGORITHM_VERSION)
            print("Claves eliminadas. La BD queda lista para el siguiente ciclo.")
        else:
            print("Claves conservadas en BD.")

    def _registrar_analisis(self):
        from domain.analysis_result import AnalysisResult
        from datetime import datetime
        import uuid

        print("\n— Registrar resultado de análisis externo —")
        print(f"Versión actual: {ALGORITHM_VERSION}")
        try:
            sample_size = int(input("Tamaño de muestra analizada: "))
            passed_raw = input("Tests pasados (separados por coma, ej: frequency,runs,serial): ")
            passed_tests = [t.strip() for t in passed_raw.split(",") if t.strip()]
            notes = input("Notas (opcional): ").strip()

            result = AnalysisResult(
                result_id=str(uuid.uuid4())[:8],
                timestamp=datetime.now(),
                algorithm_version=ALGORITHM_VERSION,
                sample_size=sample_size,
                p_values={},
                passed_tests=passed_tests,
                notes=notes
            )
            self.repo.save_result(result)
            print(f"Análisis registrado para versión {ALGORITHM_VERSION}.")
        except ValueError:
            print("Valor no válido.")

    def _api(self):
        print("\nArrancando servidor API en http://localhost:8000 ...")
        print("(FastAPI pendiente de implementar)")

    def _estado(self):
        total = self.repo.count_keys_by_version(ALGORITHM_VERSION)
        print("\n— Estado del sistema —")
        print(f"  Cámara:         {'Conectada' if self.camera.cap and self.camera.cap.isOpened() else 'Desconectada'}")
        print(f"  Base de datos:  {'Conectada' if self.repo.conn else 'Desconectada'}")
        print(f"  Generación:     {'EN CURSO' if self._generando else 'parada'}")
        print(f"  Versión actual: {ALGORITHM_VERSION}")
        print(f"  Claves en BD:   {total}")

        resultados = self.repo.get_all_results()
        if resultados:
            print(f"  Análisis guardados: {len(resultados)}")
            for r in resultados:
                estado = f"{len(r.passed_tests)} tests pasados"
                print(f"    [{r.algorithm_version}] {r.timestamp.strftime('%d/%m %H:%M')} — {estado} — {r.notes or 'sin notas'}")

    def _salir(self):
        if self._generando:
            print("Parando generación antes de salir...")
            self._generando = False
            self._hilo.join(timeout=5)
        self.camera.release()
        self.repo.release()
        print("Hasta luego.")