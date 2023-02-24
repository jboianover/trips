# Trips Data Ingestion and Analysis
This is a Python-based solution for ingesting and analyzing trips data. It uses an API endpoint to automate the on-demand data ingest and stores the data in a PostgresSQL database. The solution is designed to be scalable to handle up to 100 million entries.

## Prerequisites
- Docker
- Docker Compose
- Web browser

## Getting Started
1. Clone the repository to your local machine:

```bash
git clone https://github.com/example/trips-data-ingestion-python.git
```

2. Navigate to the project directory:
```bash
cd trips
```

3. We already have a **`.env`** file in the project directory with the necessary environment variables:

```makefile
DATABASE_URL=postgresql://admin:admin@postgres_host:5432/trips_challenge
FLASK_APP=app.py
DOCKER_DEFAULT_PLATFORM=linux/amd64
PORT=5005
```
You can modify the values as needed. These values will be used by the Docker Compose file to configure the PostgresSQL database.

4. Build and start the Docker containers using Docker Compose:
```bash
docker-compose up --d
```

This command will build and start the Python and PostgresSQL containers. The Flask API inside one of the containers will automatically start.
The data ingest script will have to be invoked manually from inside the app container.

5. Get into the app container to find the data_ingestion.py file:

```bash
docker exec -ti trips-app-1 /bin/bash
```

This command will get you into the app container where you should find the script to be run and then you will have to manually run the it. 
```bash
python data_ingestion.py
```

You will be able to monitor the status of the data ingest from the logs within the /logs folder.
```bash
cd /logs
```
6. Access the API endpoint:

```bash
http://localhost:5005/trips
```
This endpoint will return a JSON response containing the full list of trips.

```bash
http://localhost:5005/trips?region=some_region
```
This endpoint will return a JSON response containing the full list of trips for the specified region.

```bash
http://localhost:5005/trips?date=some_date_in_YYYY-MM-DD
```
This endpoint will return a JSON response containing the full list of trips for the specified date.

```bash
http://localhost:5005/average_trips?region=some_region&start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
```
This endpoint will return a JSON response containing the list of the average number of trips for the specified region.

##Configuration
The configuration for the data ingest script can be modified by changing the values in the **`config.yml`** file.

## Scaling
This solution is designed to be scalable to handle up to 100 million entries. The PostgresSQL database is used to store the data, and it can be easily scaled by adding more database nodes. The Docker Compose file can be modified to add more database nodes.
Also the code is prepared to iterate through big csv files and read them in chunks son pandas doesn't affect the memory usage.

## License
Free.