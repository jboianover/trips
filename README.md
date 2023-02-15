# Trips Data Ingestion and Analysis
This is a Python-based solution for ingesting and analyzing trips data. It uses an API endpoint to automate the on-demand data ingest and stores the data in a PostgresSQL database. The solution is designed to be scalable to handle up to 100 million entries.

## Prerequisites
- Python 3.10 or higher
- Docker
- Docker Compose

## Getting Started
1. Clone the repository to your local machine:

```bash
git clone https://github.com/example/trips-data-ingestion-python.git
```

2. Navigate to the project directory:
```bash
cd trips-data-ingestion-python
```

3. Create a **`.env`** file in the project directory and add the following environment variables:

```makefile
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secret
POSTGRES_DB=trips
POSTGRES_HOST=db
```
You can modify the values as needed. These values will be used by the Docker Compose file to configure the PostgresSQL database.

4. Build and start the Docker containers using Docker Compose:
```bash
docker-compose up --build
```

This command will build and start the Python and PostgresSQL containers. The data ingest script will start running as soon as the containers are up and running.

5. Check the data ingestion status:

```bash
docker-compose logs -f ingest
```
This command will show the logs for the data ingestion script. You can monitor the status of the data ingest from these logs.

6. Access the API endpoint:

```bash
http://localhost:5000/trips
```
This endpoint will return a JSON response containing the weekly average number of trips for the specified area (defined by a bounding box or region).

##Configuration
The configuration for the data ingest script can be modified by changing the values in the **`config.yml`** file.

## Scaling
This solution is designed to be scalable to handle up to 100 million entries. The PostgresSQL database is used to store the data, and it can be easily scaled by adding more database nodes. The Docker Compose file can be modified to add more database nodes.

## License
Free.