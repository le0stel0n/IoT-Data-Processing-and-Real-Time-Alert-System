from kafka import KafkaConsumer
import json

# Kafka Consumer
consumer = KafkaConsumer(
    'gps_stream',  # Topic to subscribe to
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Consume and print data
print("Listening for IoT data...")
for message in consumer:
    print(f"Received: {message.value}")
