# Weather-Data-ETL
 Analyzing global weather data using an AWS ETL pipeline
# 🌦️ Weather Data ETL Pipeline

## 📌 Project Overview
This project is an **AWS-based ETL pipeline** that fetches **real-time weather data** from an API every **12 minutes**, transforms it, and loads it into **Amazon Redshift** for analytics. The data is later visualized using **Amazon QuickSight**.

## 🏗️ Architecture

- **AWS S3** -            ``Stores raw and processed data``
- **AWS Lambda** -        ```Handles JSON to CSV conversion and Redshift loading```
- **Amazon Redshift** -   ``Stores structured weather data for analytics``
- **Amazon QuickSight** - ``Data visualization``

## 📂 Project Structure

## 🚀 Getting Started

### a. Clone the Repository

bash

```git clone https://github.com/your-username/weather-data-etl.git```

```cd weather-data-etl```

### b.  Install Dependencies

```pip install -r requirements.txt```

### c. Set Up AWS Credentials

```Ensure you have an AWS IAM role with permissions for S3, Lambda, Glue, and Redshift.```

### d.Follow the below steps.

## **Steps to Build the Weather Data ETL Pipeline on AWS**  

### **1. Create an S3 Bucket for Raw Data Storage**  
- Navigate to the **Amazon S3** console and create a new bucket named **`fetched-data`**.  
- This bucket will store raw weather data in **JSON format**.  

### **2. Create a Lambda Function (`fetch_weather`) for Data Ingestion**  
- Develop a **Lambda function** named **`fetch_weather`** to fetch weather data from an external API.  
- Use the **ETL script** provided in the project (`fetch_weather.py`).  

### **3. Configure IAM Role for Lambda Execution**  
- Create an **IAM role** named **`fetch_weather_lambda_role`**.  
- Assign the following permissions:  
  - **S3 write access** to allow Lambda to write data to `fetched-data`.  
  - **Basic Lambda execution permissions**.  
- Attach this IAM role to the **`fetch_weather` Lambda function**.  

### **4. Test the Lambda Function**  
- Save and test the function.  
- Verify that weather data is successfully written to the **`fetched-data`** S3 bucket.  

### **5. Automate Data Ingestion Using Amazon EventBridge**  
- Navigate to **Amazon EventBridge** and create a **scheduled rule**:  
  - **Rule Name**: `fetch_weather_schedule`  
  - **Rule Type**: **Schedule**  
  - **Schedule Pattern**: **Rate-based (e.g., every 15 minutes)**  
  - **Target**: AWS Lambda (`fetch_weather`)  
- Create a new **IAM role** for EventBridge and assign it the **Lambda execution policy**.  
- Save and enable the rule.  

### **6. Verify Automated Execution**  
- Confirm that the **`fetch_weather` Lambda function** is triggered every 15 minutes.  
- Check the **S3 bucket (`fetched-data`)** to ensure JSON data is being written.  

### **7. Convert JSON Data to CSV Format**  
- Create another **Lambda function** named **`convert_json_to_csv`** to process and transform the JSON data into CSV.  
- Assign a new **IAM role** to this Lambda function with:  
  - **S3 full access** to read from `fetched-data` and write to a new bucket.  

### **8. Create a Separate S3 Bucket for Processed CSV Data**  
- Create another **S3 bucket** named **`csv-data`** to store the converted CSV files.  

### **9. Automate JSON to CSV Conversion**  
- Set up **S3 Event Notifications** on the `fetched-data` bucket:  
  - **Event Type**: `PUT`  
  - **Destination**: AWS Lambda  
  - **Lambda Function**: `convert_json_to_csv`  
- Modify the IAM role associated with `fetched-data` to include **Lambda execution permissions**.  

### **10. Verify JSON to CSV Conversion**  
- When new JSON files arrive in `fetched-data`, the **`convert_json_to_csv`** Lambda function should be triggered.  
- The processed CSV files should appear in the **`csv-data`** bucket.  

### **11. Load Processed Data into Amazon Redshift**  
- Set up an **Amazon Redshift cluster** with minimal configuration.  
- Note down the **database credentials** for connection.  

### **12. Create a Lambda Function to Load Data into Redshift**  
- Develop a new **Lambda function** named **`load_to_redshift`**.  
- Assign a new **IAM role** with:  
  - **S3 full access** (to read from `csv-data`).  
  - **Redshift full access** (to insert data into Redshift).  
- Update the **Lambda trust relationships** to include both **Lambda and Redshift** services.  

### **13. Automate Data Loading into Redshift**  
- Set up an **S3 Event Notification** on the `csv-data` bucket:  
  - **Event Type**: `PUT`  
  - **Destination**: AWS Lambda  
  - **Lambda Function**: `load_to_redshift`  
- Modify the IAM role associated with `csv-data` to include **Lambda execution permissions**.  

### **14. Create Redshift Table and Schema**  
- Navigate to the **Amazon Redshift Query Editor** and establish a connection to the database.  
- Execute the **SQL script** to create a **table schema** for storing weather data.  

### **15. Verify Data Loading in Redshift**  
- Run the following SQL query to check if data has been successfully loaded:  
  ```sql
  SELECT * FROM weather_data;
  ```  

### **Final Outcome**  
- The pipeline **automatically** fetches, processes, and loads weather data into **Amazon Redshift**.  
- The data is **ready for analytics and visualization** using tools like **Amazon QuickSight**.  



