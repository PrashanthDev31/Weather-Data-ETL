import json
import csv
import boto3
import os
from io import StringIO
s3 = boto3.client("s3")
def lambda_handler(event, context):
    record = event["Records"][0]
    source_bucket = record["s3"]["bucket"]["name"]
    json_file_key = record["s3"]["object"]["key"]
    target_bucket = "json-csv-data"
    csv_file_key = json_file_key.replace(".json", ".csv")  
    try:
        # Fetch JSON file from S3
        response = s3.get_object(Bucket=source_bucket, Key=json_file_key)
        json_content = response["Body"].read().decode("utf-8")
        data = json.loads(json_content)  
        # Flatten and extract required fields
        extracted_data = {
            "lon": data["coord"]["lon"],
            "lat": data["coord"]["lat"],
            "weather_id": data["weather"][0]["id"] if data["weather"] else None,
            "weather_main": data["weather"][0]["main"] if data["weather"] else None,
            "weather_desc": data["weather"][0]["description"] if data["weather"] else None,
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "temp_min": data["main"]["temp_min"],
            "temp_max": data["main"]["temp_max"],
            "pressure": data["main"]["pressure"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "wind_deg": data["wind"]["deg"],
            "clouds_all": data["clouds"]["all"],
            "dt": data["dt"],
            "city_name": data["name"]
        }
        # Convert to CSV
        csv_buffer = StringIO()
        fieldnames = extracted_data.keys()
        writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(extracted_data)
        # Upload CSV to S3
        s3.put_object(
            Bucket=target_bucket,
            Key=csv_file_key,
            Body=csv_buffer.getvalue(),
            ContentType="text/csv"
        )
        print(f"Successfully converted {json_file_key} to {csv_file_key} and stored in {target_bucket}")
        return {"statusCode": 200, "message": "Success"}
    except Exception as e:
        print(f"Error processing {json_file_key}: {str(e)}")
        return {"statusCode": 500, "message": str(e)}
