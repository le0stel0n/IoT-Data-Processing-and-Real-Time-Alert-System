from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType
from influxdb_client import InfluxDBClient, QueryApi
from pyspark.sql.functions import col, avg, max

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Query IoT Data from InfluxDB") \
    .getOrCreate()

print("Spark Session Initialized")

# Replace with your provided credentials
bucket = "Iot_data"
org = "University of Colorado Boulder"
token = "q5wLN9OnCHYmdBM-xPV-55K-NfYL_GXvjxPlLfdmrq8frCgTB2wtT8Oz1W_dC8WOdUYi7_f6XH9SGlvcBqsr0w=="
url = "http://localhost:8086"

# Connect to InfluxDB
client = InfluxDBClient(url=url, token=token)
query_api = client.query_api()

# Query data from InfluxDB
query = f'from(bucket: "{bucket}") |> range(start: -24h)'
tables = query_api.query(org=org, query=query)

# Prepare data for Spark
data = []
iot_records = {}  # To store combined fields for each Sensor_ID and Timestamp

print("Raw Data from InfluxDB:")
for record in tables:
    for entry in record.records:
        print(entry.values)  # Debug: Print raw record values
        
        # Extract fields
        sensor_id = int(entry.values.get("Sensor_ID")) if entry.values.get("Sensor_ID") else None
        timestamp = entry.values.get("_time")
        if timestamp:
            timestamp_spark = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        else:
            timestamp_spark = None
        field = entry.values.get("_field")
        value = entry.values.get("_value")

        # Combine fields for the same Sensor_ID and Timestamp
        if (sensor_id, timestamp_spark) not in iot_records:
            iot_records[(sensor_id, timestamp_spark)] = {
                "Sensor_ID": sensor_id,
                "Timestamp": timestamp_spark,
                "Latitude": None,
                "Longitude": None,
                "Temperature": None,
                "Humidity": None,
                "Speed": None,
            }
        if field and value is not None:
            iot_records[(sensor_id, timestamp_spark)][field] = value

# Convert records to list of dictionaries
data = list(iot_records.values())

print(f"Data Prepared for Spark: {data[:10]}")  # Print first 10 records

# Define schema for Spark DataFrame
schema = StructType([
    StructField("Sensor_ID", IntegerType(), True),
    StructField("Timestamp", StringType(), True),
    StructField("Latitude", FloatType(), True),
    StructField("Longitude", FloatType(), True),
    StructField("Temperature", FloatType(), True),
    StructField("Humidity", FloatType(), True),
    StructField("Speed", FloatType(), True),
])
#SparkTransformation
# Create Spark DataFrame
iot_df = spark.createDataFrame(data, schema=schema)

print("Displaying DataFrame Contents:")
iot_df.show(truncate=False)

avg_temp_df = iot_df.groupBy("Latitude", "Longitude").agg(avg("Temperature").alias("Avg_Temperature"))
print("Average Temperature by Region:")
avg_temp_df.show(truncate=False)

# 2. Maximum Speed by Sensor ID
max_speed_df = iot_df.groupBy("Sensor_ID").agg(max("Speed").alias("Max_Speed"))
print("Maximum Speed by Sensor ID:")
max_speed_df.show(truncate=False)

# 3. Threshold-Based Filtering
# filtered_df = iot_df.filter((col("Temperature") > 40) | (col("Speed") > 100))
# print("Rows with Temperature > 40 or Speed > 100:")
# filtered_df.show(truncate=False)

avg_temp_csv_path = "average_temperature_by_region"
avg_temp_df.write.csv(avg_temp_csv_path, header=True, mode="overwrite")
print(f"Average Temperature data saved as CSV at: {avg_temp_csv_path}")

max_speed_csv_path = "maximum_speed_by_sensor_id"
max_speed_df.write.csv(max_speed_csv_path, header=True, mode="overwrite")
print(f"Maximum Speed data saved as CSV at: {max_speed_csv_path}")

iot_csv_path = "transformed_iot_data"
iot_df.write.csv(iot_csv_path, header=True, mode="overwrite")
print(f"Transformed IoT data saved as CSV at: {iot_csv_path}")

# Stop Spark session
spark.stop()
