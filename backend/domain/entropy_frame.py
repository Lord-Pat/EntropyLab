from dataclasses import dataclass
from datetime import datetime

@dataclass
class EntropyFrame:
    timestamp: datetime
    raw_bytes: bytes