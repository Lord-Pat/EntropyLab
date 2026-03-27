from dataclasses import dataclass
from datetime import datetime

@dataclass
class Key:
    value: str
    timestamp: datetime
    algorithm_version: str
    key_id: int = None