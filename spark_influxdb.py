from pyspark.sql import SparkSession

# Start a Spark Session
spark = SparkSession.builder \
    .appName("IoT Data Analysis") \
    .config("spark.jars", "/opt/spark/jars/influxdb-java-2.23.jar") \
    .getOrCreate()

print("Spark Session Initialized")
