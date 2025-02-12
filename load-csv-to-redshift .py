import boto3
import json
import os
# Initialize AWS clients
s3 = boto3.client("s3")
secrets_client = boto3.client("secretsmanager")
redshift = boto3.client("redshift-data")
# Fetch Redshift credentials from AWS Secrets Manager
SECRET_NAME = "pass/redshift2"
def get_redshift_credentials():
    secret = secrets_client.get_secret_value(SecretId=SECRET_NAME)
    return json.loads(secret["SecretString"])
# Load credentials
db_credentials = get_redshift_credentials()
# Redshift Configuration
REDSHIFT_CLUSTER_ID = db_credentials["cluster_id"]
REDSHIFT_DATABASE = db_credentials["dbname"]
REDSHIFT_DB_USER = db_credentials["username"]
IAM_ROLE = "arn:aws:iam::011528301337:role/s3-redshift"
S3_BUCKET = "json-csv-data"
REDSHIFT_TABLE = "weather_data"
def check_if_dt_exists(dt_value):
    """Check if the given dt exists in the Redshift table."""
    query = f"SELECT COUNT(*) FROM {REDSHIFT_TABLE} WHERE dt = {dt_value};"
    
    response = redshift.execute_statement(
        ClusterIdentifier=REDSHIFT_CLUSTER_ID,
        Database=REDSHIFT_DATABASE,
        DbUser=REDSHIFT_DB_USER,
        Sql=query
    )
    # Wait for query execution to complete
    query_id = response["Id"]
    while True:
        result = redshift.describe_statement(Id=query_id)
        if result["Status"] in ["FINISHED", "FAILED", "ABORTED"]:
            break
    if result["Status"] == "FINISHED":
        records = redshift.get_statement_result(Id=query_id)
        count = int(records["Records"][0][0]["longValue"])
        return count > 0  # True if dt exists
    return False  # Assume dt doesn't exist if query fails
def lambda_handler(event, context):
    try:
        # Extract S3 file info
        record = event["Records"][0]
        s3_file_key = record["s3"]["object"]["key"]
        s3_path = f"s3://{S3_BUCKET}/{s3_file_key}"
        # Read CSV data to find dt value
        response = s3.get_object(Bucket=S3_BUCKET, Key=s3_file_key)
        csv_content = response["Body"].read().decode("utf-8").split("\n")
        
        # Extract dt from the first data row (assuming first row is headers)
        first_data_row = csv_content[1].split(",")  # Get first data row
        dt_value = first_data_row[14]  # Assuming dt is in the 15th column
        # Check if this dt already exists
        if check_if_dt_exists(dt_value):
            print(f"Skipping {s3_file_key} as dt={dt_value} already exists in Redshift.")
            return {"statusCode": 200, "message": "Duplicate dt detected, skipping insertion."}
        # SQL COPY command to load data into Redshift
        copy_sql = f"""
        COPY {REDSHIFT_TABLE}
        FROM '{s3_path}'
        IAM_ROLE '{IAM_ROLE}'
        FORMAT AS CSV
        IGNOREHEADER 1
        DELIMITER ','
        REGION 'us-east-1';
        """
        # Execute Redshift COPY command
        response = redshift.execute_statement(
            ClusterIdentifier=REDSHIFT_CLUSTER_ID,
            Database=REDSHIFT_DATABASE,
            DbUser=REDSHIFT_DB_USER,
            Sql=copy_sql
        )
        print(f"Redshift COPY command executed: {response}")
        return {"statusCode": 200, "message": "Data loaded into Redshift"}
    except Exception as e:
        print(f"Error loading {s3_file_key} into Redshift: {str(e)}")
        return {"statusCode": 500, "message": str(e)}
