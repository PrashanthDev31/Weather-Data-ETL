# Weather-Data-ETL
 Analyzing global weather data using an AWS ETL pipeline
# 🌦️ Weather Data ETL Pipeline

## 📌 Project Overview
This project is an **AWS-based ETL pipeline** that fetches **real-time weather data** from an API every **12 minutes**, transforms it, and loads it into **Amazon Redshift** for analytics. The data is later visualized using **Amazon QuickSight**.

## 🏗️ Architecture
- **AWS S3** - Stores raw and processed data
- **AWS Lambda** - Handles JSON to CSV conversion and Redshift loading
- **Amazon Redshift** - Stores structured weather data for analytics
- **Amazon QuickSight** - Data visualization

## 📂 Project Structure

## 🚀 Getting Started

### 1️⃣ Clone the Repository

bash
```git clone https://github.com/your-username/weather-data-etl.git```

```cd weather-data-etl```

### 2️⃣ Install Dependencies
```pip install -r requirements.txt```

3️⃣ Set Up AWS Credentials
```Ensure you have an AWS IAM role with permissions for S3, Lambda, Glue, and Redshift.```

4️⃣ Run ETL Scripts
```Fetch weather data and process it:```

```python scripts/fetch_weather.py```

```python scripts/convert_json_to_csv.py```

``` python scripts/load_to_redshift.py```

📊 Queries for Analytics

``` SELECT city_name, AVG(temp) FROM weather_data GROUP BY city_name;```

