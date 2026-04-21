import threading
from infrastructure.csv_exporter import CSVExporter
from config import ALGORITHM_VERSION, GENERATION_LIMIT

class CLI:

    def __init__(self, key_svc, repo, camera, analysis_svc):
        self.key_svc = key_svc
        self.repo = repo
        self.camera = camera
        self.analysis_svc = analysis_svc
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
        
        total_actual = self.repo.count_keys_by_version(ALGORITHM_VERSION)

        if total_actual >= GENERATION_LIMIT:
            print(f"Ya tienes {total_actual:,} claves de la versión {ALGORITHM_VERSION}.")
            confirmacion = input("¿Seguro que quieres generar más? (s/n): ").strip().lower()
            if confirmacion != "s":
                return

        self._generando = True
        self._hilo = threading.Thread(target=self._bucle_generacion, daemon=True)
        self._hilo.start()
        print(f"Generación iniciada (versión {ALGORITHM_VERSION}). Vuelve al menú para pararla, de lo contrario parará automáticamente al llegar a {GENERATION_LIMIT} claves.")

    def _bucle_generacion(self):
        contador = 0

        while self._generando:
            total = self.repo.count_keys_by_version(ALGORITHM_VERSION)
            if total >= GENERATION_LIMIT:
                print(f"\n  [✓] Límite de {GENERATION_LIMIT:,} claves alcanzado. Generación completada.")
                self._generando = False
                break
            try:
                key = self.key_svc.generate()
                contador += 1
                if contador % 50 == 0:
                    print(f"  [{total:,} / {GENERATION_LIMIT:,}] última: {key.value}")
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
        total = self.repo.count_keys_by_version(ALGORITHM_VERSION)
        if total < 1000:
            print(f"Solo hay {total} claves. Genera al menos 1000 antes de analizar.")
            return
        self.analysis_svc.analizar(ALGORITHM_VERSION)

    def _api(self):
        import uvicorn
        from interfaces.api import app, init
        init(self.key_svc)
        print("\nServidor API en http://localhost:8000")
        uvicorn.run(app, host="0.0.0.0", port=8000)
        
    def _estado(self):
        total = self.repo.count_keys_by_version(ALGORITHM_VERSION)
        print("\n— Estado del sistema —")
        print(f"  Cámara:         {'Conectada' if self.camera.cap and self.camera.cap.isOpened() else 'Desconectada'}")
        print(f"  Base de datos:  {'Conectada' if self.repo.conn else 'Desconectada'}")
        print(f"  Generación:     {'EN CURSO' if self._generando else 'parada'}")
        print(f"  Versión actual: {ALGORITHM_VERSION}")
        print(f"  Claves en BD:   {total}")

        nist_results = self.repo.get_all_nist_results()
        shannon_results = self.repo.get_all_shannon_results()
        autocorr_results = self.repo.get_all_autocorrelation_results()
        maurer_results = self.repo.get_all_maurer_results()

        if nist_results:
            print(f"\n  Análisis NIST guardados: {len(nist_results)}")
            for r in nist_results:
                print(f"    [{r.algorithm_version}] {r.timestamp.strftime('%d/%m %H:%M')} — {r.notes or 'sin notas'}")

        if shannon_results:
            print(f"\n  Análisis Shannon guardados: {len(shannon_results)}")
            for r in shannon_results:
                print(f"    [{r.algorithm_version}] {r.timestamp.strftime('%d/%m %H:%M')} — {r.notes or 'sin notas'}")

        if autocorr_results:
            print(f"\n  Análisis Autocorrelación guardados: {len(autocorr_results)}")
            for r in autocorr_results:
                print(f"    [{r.algorithm_version}] {r.timestamp.strftime('%d/%m %H:%M')} — {r.notes or 'sin notas'}")

        if maurer_results:
            print(f"\n  Análisis Maurer guardados: {len(maurer_results)}")
            for r in maurer_results:
                print(f"    [{r.algorithm_version}] {r.timestamp.strftime('%d/%m %H:%M')} — {r.notes or 'sin notas'}")

    def _salir(self):
        if self._generando:
            print("Parando generación antes de salir...")
            self._generando = False
            self._hilo.join(timeout=5)
        self.camera.release()
        self.repo.release()
        print("Hasta luego.")