from dataclasses import dataclass
from datetime import datetime

@dataclass
class ShannonResult:
    result_id: str
    timestamp: datetime
    algorithm_version: str
    sample_size: int
    shannon: float
    notes: str = None