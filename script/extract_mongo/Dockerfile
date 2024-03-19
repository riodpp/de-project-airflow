# Use an official Python runtime as a parent image
FROM python:3.10-slim-bullseye

# Set the working directory in the container to /app
WORKDIR /app

# Add current directory files to /app in container
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the script when the container launches
CMD ["python", "extract_mongo_clickhouse.py"]