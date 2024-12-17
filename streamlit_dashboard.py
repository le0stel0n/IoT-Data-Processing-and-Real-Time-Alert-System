import streamlit as st
import pika
import json

# Function to receive messages from RabbitMQ
def consume_alerts():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='alerts')

    alerts = []

    def callback(ch, method, properties, body):
        alert = json.loads(body)
        alerts.append(alert)
        st.write(f"Received Alert: {alert}")

    channel.basic_consume(queue='alerts', on_message_callback=callback, auto_ack=True)
    st.write("Waiting for alerts...")
    channel.start_consuming()

# Streamlit UI
st.title("IoT Alerts Dashboard")
if st.button("Start Listening for Alerts"):
    consume_alerts()
