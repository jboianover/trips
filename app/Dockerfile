# Use a Python base image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file and install the dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install --upgrade psycopg2-binary
# RUN pip install --upgrade SQLAlchemy

# Copy the Flask app code
COPY app.py .

# Expose the API port
EXPOSE 5005

# Start the Flask app
CMD [ "python", "app.py" ]
