from kafka import KafkaConsumer
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import json

# Kafka Consumer setup
consumer = KafkaConsumer(
    'gps_stream',  # Topic to subscribe to
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# InfluxDB setup
bucket = "Iot_data"
org = "University of Colorado Boulder"
token = "q5wLN9OnCHYmdBM-xPV-55K-NfYL_GXvjxPlLfdmrq8frCgTB2wtT8Oz1W_dC8WOdUYi7_f6XH9SGlvcBqsr0w=="  # Replace with your InfluxDB token
url = "http://localhost:8086"  # InfluxDB URL

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Listen for messages and write to InfluxDB
print("Listening for IoT data...")
for message in consumer:
    data = message.value
    print(f"Writing to InfluxDB: {data}")
    
    # Create a Point object for InfluxDB
    point = (
        Point("iot_sensor_data")
        .tag("Sensor_ID", data["Sensor_ID"])
        .field("Latitude", data["Latitude"])
        .field("Longitude", data["Longitude"])
        .field("Temperature", data["Temperature"])
        .field("Humidity", data["Humidity"])
        .field("Speed", data["Speed"])
        .time(data["Timestamp"], WritePrecision.NS)
    )
    
    # Write the point to InfluxDB
    write_api.write(bucket=bucket, org=org, record=point)
