from dataclasses import dataclass
from typing import Optional


@dataclass
class Interaction:
    from_device: str
    to_device: str
    method: str
    bluetooth_version: str
    signal_strength_dbm: int
    distance_meters: float
    duration_seconds: int
    timestamp: str
    id: Optional[str] = None
