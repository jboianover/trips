from typing import List
from database import region_db
from model.region import Region


def lists() -> List[Region]:
    return region_db.list_all()
