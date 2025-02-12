import json
import boto3
import requests
import os
from datetime import datetime
# AWS S3 setup
S3_BUCKET_NAME = "api-fetched-data"  # Replace with your bucket name
S3_OBJECT_KEY = f"weather_data_{datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')}.json"
# OpenWeatherMap API setup
API_KEY = "172695341c73abb0940e7214abb43293"  # Replace with your API key
CITY = "Baltimore"  # Change this to your preferred city
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"
# Initialize AWS S3 client
s3_client = boto3.client("s3")
def lambda_handler(event, context):
    try:
        # Fetch weather data
        response = requests.get(URL)
        data = response.json()
        # Upload data to S3
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=S3_OBJECT_KEY,
            Body=json.dumps(data, indent=4)
        )
        print(f"Weather data saved to S3: {S3_OBJECT_KEY}")
        return {"statusCode": 200, "body": "Weather data saved successfully!"}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"statusCode": 500, "body": str(e)}


