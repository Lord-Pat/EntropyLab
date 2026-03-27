import uuid
from datetime import datetime
from services.entropy_service import EntropyService
from infrastructure.sqlite_repository import SQLiteRepository
from domain.key import Key
from config import ALGORITHM_VERSION

class KeyGeneratorService:

    def __init__(self, entropy_service, repository):
        self.entropy_service = entropy_service
        self.repository = repository

    def generate(self):
        entropy_bytes = self.entropy_service.extract_entropy()

        value = str(uuid.UUID(bytes=entropy_bytes[:16]))

        # usamos solo los 16 primeros, que es lo que necesitamos para nuestra clave GUID estándar
        # esto nos permite en un futuro tocal esta parte para escalar la complejidad de las claves 

        key = Key(
            value=value,
            timestamp=datetime.now(),
            algorithm_version=ALGORITHM_VERSION
        )

        self.repository.save_key(key)
        return key