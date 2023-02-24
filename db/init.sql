CREATE DATABASE trips_challenge;

CREATE TABLE stage_trip (
  region VARCHAR(100),
  vehicle VARCHAR(100),
  origin_lat DOUBLE PRECISION NOT NULL, 
  origin_long DOUBLE PRECISION NOT NULL, 
  dest_lat DOUBLE PRECISION NOT NULL, 
  dest_long DOUBLE PRECISION NOT NULL, 
  date DATE NOT NULL, 
  time TIME(6) WITHOUT TIME ZONE NOT NULL);

CREATE TABLE trip (
  id SERIAL NOT NULL, 
  region VARCHAR(100),
  vehicle VARCHAR(100),
  origin_lat DOUBLE PRECISION NOT NULL, 
  origin_long DOUBLE PRECISION NOT NULL, 
  dest_lat DOUBLE PRECISION NOT NULL, 
  dest_long DOUBLE PRECISION NOT NULL, 
  date DATE NOT NULL, 
  time TIME(6) WITHOUT TIME ZONE NOT NULL, PRIMARY KEY (id));



CREATE INDEX idx_trip_origin_lat_lon ON trips (origin_lat, origin_long);
CREATE INDEX idx_trip_dest_lat_lon ON trips (dest_lat, dest_long);
CREATE INDEX idx_trips_end_time ON trip (date);