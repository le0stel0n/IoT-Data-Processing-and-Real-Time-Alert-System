import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

# Define the callback function to process messages from the queue
def callback(ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
    """
    Callback function to process received messages.

    Args:
        ch (BlockingChannel): The channel object that invoked the callback.
        method (Basic.Deliver): Metadata about the delivery.
        properties (BasicProperties): Message properties.
        body (bytes): The actual message payload.
    """
    message = body.decode('utf-8')  # Decode the message body from bytes to string
    print(f" [x] Received: {message}")

# Establish connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # Replace with appropriate hostname
channel = connection.channel()

# Declare the queue (ensure it exists)
channel.queue_declare(queue='alerts')

# Set up the consumer
channel.basic_consume(
    queue='alerts',  # Queue name
    on_message_callback=callback,  # Callback function to process messages
    auto_ack=True  # Automatically acknowledge messages
)

print(' [*] Waiting for messages. To exit press CTRL+C')

# Start consuming messages
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("\n [x] Exiting...")
    connection.close()
