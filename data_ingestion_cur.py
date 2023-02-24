import os
import csv
import psycopg2
from psycopg2.extras import execute_values

# Configuration parameters
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'mydb')
DB_USER = os.getenv('DB_USER', 'myuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'mypassword')
TABLE_NAME = 'trips'
DATA_DIR = 'data'

# Connect to PostgresSQL
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cur = conn.cursor()

# Create table if not exists
cur.execute(f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    trip_id SERIAL PRIMARY KEY,
    pickup_datetime TIMESTAMP NOT NULL,
    pickup_longitude FLOAT NOT NULL,
    pickup_latitude FLOAT NOT NULL,
    dropoff_longitude FLOAT NOT NULL,
    dropoff_latitude FLOAT NOT NULL,
    passenger_count INTEGER NOT NULL
)''')

# Ingest data from CSV files
for file_name in os.listdir(DATA_DIR):
    if not file_name.endswith('.csv'):
        continue
    file_path = os.path.join(DATA_DIR, file_name)
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # skip header
        rows = [(row[0], *map(float, row[1:5]), int(row[5])) for row in csv_reader]
        execute_values(cur, f'''INSERT INTO {TABLE_NAME} (
            pickup_datetime,
            pickup_longitude,
            pickup_latitude,
            dropoff_longitude,
            dropoff_latitude,
            passenger_count
        ) VALUES %s''', rows)
        conn.commit()

# Close database connection
cur.close()
conn.close()
