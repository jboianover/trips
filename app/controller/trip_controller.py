from typing import List
from database import trip_db
from model.trip import Trip


def lists() -> List[Trip]:
    return trip_db.list_all()


def filter_by_date(date) -> List[Trip]:
    return trip_db.filter_by_date(date)


def filter_by_region(region) -> List[Trip]:
    return trip_db.filter_by_region(region)


def average_trips(region, start_date, end_date) -> List[Trip]:
    return trip_db.average_trips(region, start_date, end_date)
