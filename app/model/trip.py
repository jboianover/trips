from typing import NamedTuple
from datetime import datetime


class Trip(NamedTuple):
    id: int = None
    region: str = None
    vehicle: str = None
    origin_lat: float = None
    origin_long: float = None
    dest_lat: float = None
    dest_long: float = None
    date: datetime.date = None
    time: datetime.time = None
