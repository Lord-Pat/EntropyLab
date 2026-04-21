from dataclasses import dataclass
from datetime import datetime

@dataclass
class AutocorrelationResult:
    result_id: str
    timestamp: datetime
    algorithm_version: str
    sample_size: int
    lag1_correlation: float
    lag1_p: float
    lag8_correlation: float
    lag8_p: float
    notes: str = None