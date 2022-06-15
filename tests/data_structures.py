from dataclasses import dataclass
from typing import Optional


@dataclass
class Track:
    track_id: int
    track_type: str
    title: Optional[str]
    language: str
    default: str
    forced: str
