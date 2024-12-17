# import pika
# import json

# # Connection parameters
# connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-server'))
# channel = connection.channel()

# # Declare a queue
# channel.queue_declare(queue='alerts')

# def send_alert(sensor_id, message):
#     alert = {
#         "sensor_id": sensor_id,
#         "message": message
#     }
#     channel.basic_publish(
#         exchange='',
#         routing_key='alerts',
#         body=json.dumps(alert)
#     )
#     print(f" [x] Sent {alert}")

# # Close the connection when the script ends
# def close_connection():
#     connection.close()

import pika
import json

# Utility to get a RabbitMQ connection and channel
def get_rabbitmq_channel():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-server'))
        channel = connection.channel()
        channel.queue_declare(queue='alerts')  # Ensure the queue exists
        return connection, channel
    except Exception as e:
        print(f"[!] Failed to connect to RabbitMQ: {e}")
        raise e

# Send an alert message
def send_alert(sensor_id, message):
    try:
        connection, channel = get_rabbitmq_channel()
        alert = {
            "sensor_id": sensor_id,
            "message": message
        }
        channel.basic_publish(
            exchange='',
            routing_key='alerts',
            body=json.dumps(alert)
        )
        print(f"[x] Sent {alert}")
        channel.close()  # Close the channel
        connection.close()  # Close the connection
    except Exception as e:
        print(f"[!] Error sending alert: {e}")
        raise e

# Example usage
if __name__ == "__main__":
    send_alert(1, "Temperature exceeds 50°C")

