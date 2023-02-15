# Use a Python base image
FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file and install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code
COPY app.py .

# Expose the API port
EXPOSE 5000

# Start the Flask app
CMD [ "python", "app.py" ]
