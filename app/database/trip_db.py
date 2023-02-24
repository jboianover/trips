from database.connections import _fetch_rows
from model.trip import Trip
from typing import List


def list_all() -> List[Trip]:
    query = 'SELECT * FROM trip'
    records = _fetch_rows(query)

    trips = []
    for row in records:
        trip = Trip(
            id=row.id,
            region=row.region,
            vehicle=row.vehicle,
            origin_lat=row.origin_lat,
            origin_long=row.origin_long,
            dest_lat=row.dest_lat,
            dest_long=row.dest_long,
            date=row.date.strftime('%Y-%m-%d')
        )
        trips.append(trip)

    return trips


def average_trips(region, start_date, end_date) -> List[Trip]:

    query = (f"""
    SELECT COUNT(*) / 7 AS average_trips FROM trip
    WHERE region = '{region}'
    AND date BETWEEN '{start_date}' AND '{end_date}'""")
    records = _fetch_rows(query)
    trips = []
    for row in records:
        average_trips = row.average_trips
        trips.append(average_trips)

    return trips


def filter_by_date(date) -> List[Trip]:

    query = (f"""
    SELECT * FROM trip
    WHERE date = '{date}'
    """
             )
    records = _fetch_rows(query)

    trips = []
    for row in records:
        trip = Trip(
            id=row.id,
            region=row.region,
            vehicle=row.vehicle,
            origin_lat=row.origin_lat,
            origin_long=row.origin_long,
            dest_lat=row.dest_lat,
            dest_long=row.dest_long,
            date=row.date.strftime('%Y-%m-%d')
        )
        trips.append(trip)

    return trips


def filter_by_region(region) -> List[Trip]:

    query = (f"""
    SELECT * FROM trip
    WHERE region = '{region}'
    """
             )
    records = _fetch_rows(query)

    trips = []
    for row in records:
        trip = Trip(
            id=row.id,
            region=row.region,
            vehicle=row.vehicle,
            origin_lat=row.origin_lat,
            origin_long=row.origin_long,
            dest_lat=row.dest_lat,
            dest_long=row.dest_long,
            date=row.date.strftime('%Y-%m-%d')
        )
        trips.append(trip)

    return trips
