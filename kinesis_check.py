import boto3
import time
from botocore.exceptions import ClientError

def kinesis_check():
    # Check kinesis Stream status

    kinesis_client = boto3.client('kinesis', region_name='us-east-1')

    stream_name = 'kinesis-mobile-log-stream'

    response = kinesis_client.describe_stream(StreamName=stream_name)
    status = response['StreamDescription']['StreamStatus']
    print(f"Stream status is '{status}'")