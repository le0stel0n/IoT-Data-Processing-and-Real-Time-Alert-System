from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pathlib import Path
import pandas as pd

# Initialize FastAPI app
app = FastAPI()

# Define the paths to the folders containing the CSV files
avg_temp_csv_path = Path("average_temperature_by_region")
max_speed_csv_path = Path("maximum_speed_by_sensor_id")
iot_csv_path = Path("transformed_iot_data")

# Utility function to read multiple CSV files from a folder and combine them
def load_csv_files_from_folder(folder_path: Path):
    all_csv_files = folder_path.glob("*.csv")  # Find all CSV files in the folder
    dataframes = [pd.read_csv(file) for file in all_csv_files]  # Read each CSV file
    combined_df = pd.concat(dataframes, ignore_index=True)  # Combine into a single DataFrame
    return combined_df

# API Endpoints

@app.get("/")
def read_root():
    return {"message": "Welcome to the IoT Data API!"}

@app.get("/data/average-temperature")
def get_average_temperature():
    try:
        avg_temp_df = load_csv_files_from_folder(avg_temp_csv_path)
        return JSONResponse(content=avg_temp_df.to_dict(orient="records"))
    except Exception as e:
        return {"error": str(e)}

@app.get("/data/maximum-speed")
def get_maximum_speed():
    try:
        max_speed_df = load_csv_files_from_folder(max_speed_csv_path)
        return JSONResponse(content=max_speed_df.to_dict(orient="records"))
    except Exception as e:
        return {"error": str(e)}

@app.get("/data/iot-transformed")
def get_transformed_iot_data():
    try:
        iot_df = load_csv_files_from_folder(iot_csv_path)
        return JSONResponse(content=iot_df.to_dict(orient="records"))
    except Exception as e:
        return {"error": str(e)}


from rabbitmq_producer import send_alert

@app.get("/check-temperature")
def check_temperature():
    try:
        iot_df = load_csv_files_from_folder(iot_csv_path)  # Load the data
        alerts = []  # To store alerts

        # Check for temperatures above 25°C
        for _, row in iot_df.iterrows():
            if row["Temperature"] > 25:
                message = f"High temperature detected: {row['Temperature']}°C at Sensor {row['Sensor_ID']}"
                send_alert(row["Sensor_ID"], message)  # Send alert
                alerts.append({"sensor_id": row["Sensor_ID"], "message": message})

        if alerts:
            return {"alerts": alerts}
        return {"message": "No high temperature alerts"}
    except Exception as e:
        return {"error": str(e)}

