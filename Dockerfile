# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Define the working directory
WORKDIR /app

# Copy the requirements.txt file first to install dependencies
COPY requirements.txt /app/

# Dependencies installation
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ./app /app

# Exposing port 5000
EXPOSE 5000

# Launching Flask app
CMD ["python", "app.py"]