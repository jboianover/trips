import pandas as pd
import os
from sqlalchemy import create_engine
from io import StringIO
import logging

logging.basicConfig(filename='data_ingestion.log',
                    level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def process_raw_file(filename):

    # create engine and connect to database
    # engine = create_engine(os.environ['DATABASE_URL'])
    engine = create_engine('postgresql://admin:admin@localhost:5432/trips_challenge')
    with engine.connect() as conn:
        # iterate through the file in binary mode and read it in chunks
        try:
            with open(filename, 'rb') as f:
                # iterate over the chunks and transform the resultant dataframe
                for df in pd.read_csv(StringIO(f.read().decode()), chunksize=10000):
                    # Extract latitude and longitude from origin_coord column
                    df['origin_lat'] = df['origin_coord'].str.extract(r'POINT \((.*?)\s')
                    df['origin_long'] = df['origin_coord'].str.extract(r'POINT \(.*?\s(.*?)\)')

                    # Extract latitude and longitude from destination_coord column
                    df['dest_lat'] = df['destination_coord'].str.extract(r'POINT \((.*?)\s')
                    df['dest_long'] = df['destination_coord'].str.extract(r'POINT \(.*?\s(.*?)\)')

                    # Convert latitude and longitude to float
                    df['origin_lat'] = df['origin_lat'].astype(float)
                    df['origin_long'] = df['origin_long'].astype(float)
                    df['dest_lat'] = df['dest_lat'].astype(float)
                    df['dest_long'] = df['dest_long'].astype(float)

                    # extract the date and time from the datetime column
                    df['date'] = pd.to_datetime(df['datetime']).dt.date
                    df['time'] = pd.to_datetime(df['datetime']).dt.time

                    # Drop the original coord columns
                    df.drop(['origin_coord', 'destination_coord', 'datetime'], axis=1, inplace=True)

                    # Rename datasource column to vehicle
                    df.rename(columns={'datasource': 'vehicle'}, inplace=True)

                    # insert data into the database in chunks
                    try:
                        df.to_sql('stage_trip', con=conn, if_exists='append',
                                  index=False, chunksize=1000)
                    except Exception as e:
                        # Log a warning message
                        logging.warning("""Data ingestion has failed
                                        while writting into the stage table.
                                        """)
                        raise e
        except Exception as e:
            # Log an error message
            logging.warning('There was an error working with the csv files.')
            raise e


def extract_load_raw():
    data_dir = '/data'
    # files = os.listdir(data_dir)

    csv_files = ['/Users/jonathan.boianover/Documents/GitHub/trips/data/trips.csv']
    # csv_files = [f for f in files if f.endswith('.csv')]
    print(csv_files)
    engine = create_engine('postgresql://admin:admin@localhost:5432/trips_challenge')
    with engine.connect() as conn:
        # truncate staging table before loading all the batch of files
        conn.execute("""
        TRUNCATE TABLE stage_trip;
        """)

        # Loop over the CSV files and process each one
        for file in csv_files:
            filename = os.path.join(data_dir, file)
            process_raw_file(filename)
        try:
            # Insert the staged data into the actual trip table
            conn.execute("""
            INSERT INTO trip (region, vehicle, origin_lat, origin_long,
            dest_lat, dest_long, date, time)
            select
            distinct on (origin_lat, origin_long, dest_lat, dest_long, date, time)
            region, vehicle, origin_lat, origin_long,
            dest_lat, dest_long, date, time
            from stage_trip
            order by origin_lat, origin_long, dest_lat, dest_long, date, time ;
            """)

            # close the database connection
            conn.close()
        except Exception as e:
            # Log an error message
            logging.error('There was an error while writting into the trip table.')
            raise e


if __name__ == "__main__":
    # Log an information message
    logging.info('Starting data ingestion...')

    # Process data
    data = extract_load_raw()
