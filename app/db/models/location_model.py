from dataclasses import dataclass
from typing import Optional


@dataclass
class Location:
    latitude: float
    longitude: float
    altitude_meters: int
    accuracy_meters: int
    id: Optional[str] = None
