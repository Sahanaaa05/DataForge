

import boto3
from botocore.exceptions import ClientError




def s3_bkt_creation():

    s3_client = boto3.client('s3', region_name='us-east-1')


    bucket_name = 'data-forge-bkt1'
    file_path = 'mobile-logs-generated.csv'
    object_key = 'raw/mobile-logs-generated'
    folders = ['raw/', 'processed/', 'scripts/', 'checkpoint/', 'query-results/','PathToJar/']

    script_file_path = 'script.py'
    script_key = 'scripts/script'

    jar_file_path= 'spark-streaming-kinesis-asl_2.12-3.5.5.jar'
    jar_key = 'PathToJar/spark-streaming-kinesis-asl_2.12-3.5.5.jar'


    try:
        # Creating Bucket
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created.")
        
        # Adding Folder 
        for folder in folders:
            s3_client.put_object(Bucket=bucket_name, Key=folder)
            print(f"Folder '{folder}' created.")
        
        # Uploading Mobile logs file    
        s3_client.upload_file(file_path, bucket_name, object_key)
        print(f"File '{file_path}' uploaded to s3://{bucket_name}/{object_key}")

        #uploading script file
        s3_client.upload_file(script_file_path, bucket_name, script_key)
        print(f"File '{script_file_path}' uploaded to s3://{bucket_name}/{script_key}")


         #uploading jar file
        s3_client.upload_file(jar_file_path, bucket_name, jar_key )
        print(f"File '{jar_file_path}' uploaded to s3://{bucket_name}/{jar_key}")

            

    except ClientError as e:
        print(f"Error creating bucket: {e}")




