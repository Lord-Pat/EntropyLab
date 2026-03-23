from dataclasses import dataclass
from datetime import datetime

@dataclass
class Key:
    key_id: str
    value: str
    timestamp: datetime
    algorithm_version: str