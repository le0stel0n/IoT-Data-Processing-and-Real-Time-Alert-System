# Use an official Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and the application code
COPY requirements.txt requirements.txt
COPY main.py main.py
COPY rabbitmq_producer.py rabbitmq_producer.py

# Copy the directories containing CSV files
COPY transformed_iot_data /app/transformed_iot_data
COPY average_temperature_by_region /app/average_temperature_by_region
COPY maximum_speed_by_sensor_id /app/maximum_speed_by_sensor_id

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
