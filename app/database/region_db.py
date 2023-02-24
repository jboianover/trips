from database.connections import _fetch_rows
from model.region import Region
from typing import List


def list_all() -> List[Region]:
    query = 'SELECT * FROM regions'
    records = _fetch_rows(query)

    regions = []
    for row in records:
        region = Region(
            id=row.id,
            name=row.name,
            lat_min=row.lat_min,
            lat_max=row.lat_max,
            lon_min=row.lon_min,
            lon_max=row.lon_max,
        )
        regions.append(region)

    return regions
