
from kafka import KafkaProducer
import json
import random
import time
from datetime import datetime

# Kafka Producer
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Simulate IoT data
def generate_iot_data():
    sensor_id = random.randint(1, 10)  # Simulated Sensor_IDs
    latitude = round(random.uniform(37.0, 40.0), 6)  # Latitude
    longitude = round(random.uniform(-105.0, -102.0), 6)  # Longitude
    temperature = round(random.uniform(15.0, 30.0), 1)  # Temperature
    humidity = round(random.uniform(30, 70), 1)  # Humidity
    speed = round(random.uniform(0, 100), 1)  # Speed
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "Sensor_ID": sensor_id,
        "Timestamp": timestamp,
        "Latitude": latitude,
        "Longitude": longitude,
        "Temperature": temperature,
        "Humidity": humidity,
        "Speed": speed,
    }

# Send data to Kafka
while True:
    data = generate_iot_data()
    print(f"Sending: {data}")
    producer.send('gps_stream', value=data)  # Send data to 'gps_stream' topic
    time.sleep(2)  # Simulate 2-second intervals between data points
