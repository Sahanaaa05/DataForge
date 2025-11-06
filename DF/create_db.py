
import boto3
from botocore.exceptions import ClientError

def create_db():
    # Initialize Glue client
    glue = boto3.client('glue')

    # Define parameters

    bucket_name = 'data-forge-bkt1'
    database_name = "mobile_logs_db"
    crawler_name = "crawler-mobile-processed"
    role_name = "glue-Stream-Execution-Role"
    s3_path = f"s3://{bucket_name}/processed/"

    # Step 1: Create Database
    try:
        print(f"Creating database '{database_name}'...")
        response = glue.create_database(
            DatabaseInput={
                'Name': database_name,
                'Description': 'Database for processed mobile logs'
            }
        )
        print("Database created successfully.")
    except ClientError as e:
        print(f" Failed to create database: {e}")


    