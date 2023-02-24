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


# def get_average_trips(**data) -> List[Trip]:
#     bounding_box = data.get('bounding_box')
#    # region = data.get('region')
#     start_date = data.get['start_date']
#     end_date = data.get['end_date']

#     if bounding_box:
#         query = (
#             f"SELECT COUNT(*) / 7 AS average_trips FROM trip "
#             f"WHERE origin_lat BETWEEN {bounding_box[0]} AND {bounding_box[2]} "
#             f"AND origin_long BETWEEN {bounding_box[1]} AND {bounding_box[3]} "
#             f"AND date BETWEEN '{start_date}' AND '{end_date}'"
#         )
#     else:
#         query = (
#             f"SELECT COUNT(*) / 7 AS average_trips FROM trip "
#             f"WHERE ST_Intersects(ST_GeomFromText('{region}'), "
#             f"ST_Point(origin_lat, origin_long)) "
#             f"AND date BETWEEN '{start_date}' AND '{end_date}'"
#         )
#     records = _fetch_rows(query)

def filter_by_date(date) -> List[Trip]:

    query = (f"""
    SELECT * FROM trip
    WHERE date >= '{date}'
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
    WHERE region >= '{region}'
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