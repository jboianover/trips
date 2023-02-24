from typing import NamedTuple


class Region(NamedTuple):
    id: int = None
    name: str = None
    lat_min: float = None
    lat_max: float = None
    lon_min: float = None
    lon_max: float = None
