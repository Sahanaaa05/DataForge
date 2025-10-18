#Upload a File to S3

client = boto3.client('s3')
file_path = r'C:\workspace\git\mobile-logs.csv'
client.upload_file(
    Filename=file_path,
    Bucket='SIG-mobile_data_logs',
    Key='mobile_data_logs_backup.csv'
)
print("✅ File uploaded successfully.")