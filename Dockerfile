# Use an official Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY app.py .

# Run the script
CMD ["python", "app.py"]
