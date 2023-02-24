import pandas as pd
import os
from sqlalchemy import create_engine, text
from io import StringIO
import logging
import datetime

now = datetime.datetime.now()
# create logs directory if it doesn't exist
log_dir = os.path.join(os.getcwd(), 'logs')
if not os.path.exists('logs'):
    os.makedirs('logs')
# create a log file for each datetime the process runs
log_file = os.path.join(
    log_dir, f"data_ingestion_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')


def process_raw_file(filename):

    # create engine and connect to database
    engine = create_engine(os.environ['DATABASE_URL'])
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
                print(df)
                # insert data into the database in chunks
                try:
                    logging.info('Inserting the rows from the file to the stage_trip table.')
                    df.to_sql('stage_trip', con=engine, if_exists='append',
                              index=False, chunksize=1000)
                    logging.info('Insert successful.')
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


def extract_load_trips():
    data_dir = '/app/data-input'
    processed_dir = '/app/data-input/processed/'
    files = os.listdir(data_dir)
    # csv_files = ['/Users/jonathan.boianover/Documents/GitHub/trips/data/trips.csv']
    csv_files = [f for f in files if f.endswith('.csv')]
    logging.info(f'These are the csv files to be processed: {csv_files}.')
    # engine = create_engine('postgresql://admin:admin@localhost:5432/trips_challenge')
    engine = create_engine(os.environ['DATABASE_URL'])
    with engine.connect() as conn:
        logging.info('Truncating the stage_trip table.')
        # truncate staging table before loading all the batch of files
        conn.execute(text("""
            TRUNCATE TABLE stage_trip;
        """))
        print('delete stage_trip successful')
        conn.commit()
        # Loop over the CSV files and process each one
        print(f'csv_files: {csv_files}')
        for file in csv_files:
            filename = os.path.join(data_dir, file)
            logging.info(f'Processing the file {file}.')
            process_raw_file(filename)
            # move the file to the directory
            os.rename(filename, os.path.join(processed_dir, file))
        try:
            logging.info('Inserting data from the stage_trip to the trip table.')
            # Insert the staged data into the actual trip table
            query = ("""
            INSERT INTO trip (region, vehicle, origin_lat, origin_long,
            dest_lat, dest_long, date, time)
            select
            distinct on (origin_lat, origin_long, dest_lat, dest_long, date, time)
            region, vehicle, origin_lat, origin_long,
            dest_lat, dest_long, date, time
            from stage_trip
            order by origin_lat, origin_long, dest_lat, dest_long, date, time ;
            """)
            conn.execute(text(query))
            conn.commit()
            logging.info('Insert successful.')
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
    data = extract_load_trips()
