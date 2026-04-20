from dataclasses import dataclass
from datetime import datetime

@dataclass
class NistResult:
    result_id: str
    timestamp: datetime
    algorithm_version: str
    sample_size: int
    p_values: dict
    passed_tests: list
    notes: str = None