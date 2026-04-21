from dataclasses import dataclass
from datetime import datetime

@dataclass
class MaurerResult:
    result_id: str
    timestamp: datetime
    algorithm_version: str
    sample_size: int
    fn: float
    p_value: float
    notes: str = None