from infrastructure.camera_reader import CameraReader
from infrastructure.sqlite_repository import SQLiteRepository
from services.key_generator_service import KeyGeneratorService

class CLI:

    def __init__(self, key_svc, repo, camera):
        self.key_svc = key_svc
        self.repo = repo
        self.camera = camera

    def run(self):
        print("Sistema listo.")
        while True:
            opcion = self._menu()
            if opcion == "1":
                self._generacion_masiva()
            elif opcion == "2":
                self._api()
            elif opcion == "3":
                self._estado()
            elif opcion == "0":
                self._salir()
                break
            else:
                print("Opción no válida.")

    def _menu(self):
        print("\n╔══════════════════════════════╗")
        print("║        EntropyLab v0.1       ║")
        print("╠══════════════════════════════╣")
        print("║  1. Generación masiva        ║")
        print("║  2. Arrancar servidor API    ║")
        print("║  3. Estado del sistema       ║")
        print("║  0. Salir                    ║")
        print("╚══════════════════════════════╝")
        return input("Selecciona una opción: ").strip()

    def _generacion_masiva(self):
        try:
            cantidad = int(input("¿Cuántas claves quieres generar? "))
        except ValueError:
            print("Número no válido.")
            return

        print(f"\nGenerando {cantidad} claves...")
        for i in range(cantidad):
            key = self.key_svc.generate()
            print(f"  [{i+1}/{cantidad}] {key.value}")

        keys = self.repo.get_all_keys()
        print(f"\nTotal de claves en base de datos: {len(keys)}")

    def _api(self):
        print("\nArrancando servidor API en http://localhost:8000 ...")
        print("(FastAPI pendiente de implementar)")

    def _estado(self):
        print("\n— Estado del sistema —")
        print(f"  Cámara:        {'Conectada' if self.camera.cap and self.camera.cap.isOpened() else 'Desconectada'}")
        print(f"  Base de datos: {'Conectada' if self.repo.conn else 'Desconectada'}")

    def _salir(self):
        self.camera.release()
        self.repo.release()
        print("Hasta luego.")