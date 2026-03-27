from infrastructure.camera_reader import CameraReader
from infrastructure.sqlite_repository import SQLiteRepository
from services.entropy_service import EntropyService
from services.key_generator_service import KeyGeneratorService
from interfaces.cli import CLI

if __name__ == "__main__":
    camera = CameraReader()
    camera.connect()

    repo = SQLiteRepository()
    repo.connect()

    entropy_svc = EntropyService(camera)
    key_svc = KeyGeneratorService(entropy_svc, repo)

    cli = CLI(key_svc, repo, camera)
    cli.run()