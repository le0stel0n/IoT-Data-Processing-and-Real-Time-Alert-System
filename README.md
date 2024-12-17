# IoT Data Processing and Real-Time Alert System
This repository provides a real-time IoT data processing system that ingests, processes, and visualizes sensor data while generating alerts for specific conditions. The pipeline is built using Kafka, Apache Spark, InfluxDB, RabbitMQ, FastAPI, and Streamlit.

## Overview
The system consists of several interconnected components:

* Data Ingestion: Simulated IoT sensor data streams are generated and published to Kafka topics.
* Data Processing: Apache Spark processes and transforms the data for aggregation and analysis.
* Storage: InfluxDB stores the transformed data, making it queryable and visualizable.
* Real-Time Alerts: RabbitMQ is used for managing alerts triggered by specific conditions.
* REST API: FastAPI serves endpoints to interact with the processed data and trigger alerts.
* Visualization: Streamlit provides a user-friendly dashboard for monitoring real-time data and alerts.

Before begining here are a few software components that needs to installed locally
* Apache Spark
* Docker Desktop
* Apache Kafka 
* InfluxDB 
* Java 
* Python 

## Architecture
The architecture integrates multiple components to enable seamless data processing and real-time alerts: 

![separation](Architecture.png)

## Running the System
Setting Up Kafka for Real-Time Data Ingestion
Kafka serves as the message broker to ingest simulated IoT data.
 Download and install Kafka from [Apache Kafka Downloads](https://kafka.apache.org/downloads).

Start Kafka after installation: 
```
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
```
Create Kafka-topics:
```
bin/kafka-topics.sh --create --topic gps_stream --bootstrap-server localhost:9092
```
Generate IoT Data: Use the `iot_data_producer.py` script to simulate IoT data streams. then the `iot_data_consumer.py` to read the data that is being produced. 

##  Storing Data in InfluxDB
InfluxDB is used for storing and querying time-series data.

Run InfluxDB: Download and install InfluxDB from [InfluxDB Downloads.](https://www.influxdata.com/downloads/)

```
docker run -d -p 8086:8086 --name=influxdb influxdb:latest
```
Configure InfluxDB: 

Access the UI at http://localhost:8086, create a bucket iot_data, and generate an API token.

Store Data in InfluxDB: Use the `kafka_to_influxdb.py `consumer script to fetch data from Kafka and write it to InfluxDB.

## Processing Data with Apache Spark:

Spark handles the transformation and aggregation of IoT data.

Set Up Spark: Download and configure Spark from [Apache Spark Downloads.](https://spark.apache.org/downloads.html)

Run ETL Jobs: Use `QueryDataFromInflux.py` to process data fetched from InfluxDB and save transformed data as CSV files.

## Build the FastAPI:

start by running the docker build file
make sure to run RabbitMq and Flask in the same network as they are integrated with eachother.
```
docker network create iot-network
docker network connect iot-network rabbitmq-server
```
Run Flask App:
```
docker run -d --name flask-iot-app --network iot-network -p 8000:8000 flask-rabbitmq-app
```

## Generating Real-Time Alerts with RabbitMQ:

RabbitMQ is used to push and manage real-time alerts.

Run RabbitMQ: build the RabbitMq using the image and run it.

```
docker run -d -p 5672:5672 --network iot-network -p 15672:15672 --name rabbitmq rabbitmq:management
```

## Test the API Endpoints
Use curl or a tool like Postman to test the following endpoints:
•	Root Endpoint:
```
curl http://localhost:8000/

Expected Response: {"message": "Welcome to the IoT Data API!"}

```
•	Average Temperature:
```

curl http://localhost:8000/data/average-temperature

Expected Response: JSON data with average temperatures from average_temperature_by_region.

```
•	Maximum Speed:
```
curl http://localhost:8000/data/maximum-speed

Expected Response: JSON data with maximum speeds from maximum_speed_by_sensor_id.

```
•	Transformed IoT Data:
```
curl http://localhost:8000/data/iot-transformed

Expected Response: JSON data with the transformed IoT data from transformed_iot_data.

```
•	Temperature Alerts:
```
curl http://localhost:8000/check-temperature

```
Expected Response:
o	Alerts for temperatures exceeding 25°C:
```
{
    "alerts": [
        {
            "sensor_id": 1,
            "message": "High temperature detected: 28.7°C at Sensor 1"
        }
    ]
}

```
o	If no temperatures exceed 25°C:

    "message": "No high temperature alerts"


once you verify the API endpoints. run the `rabbitmq_producer.py` to pulll the results wheich can be later fetcher by `streamlit_dashboard.py` where the alerts are received and visulaized into a dashboard. 

