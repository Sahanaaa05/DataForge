import boto3
import time
from botocore.exceptions import ClientError


def kinesis():

    kinesis_client = boto3.client('kinesis', region_name='us-east-1')

    stream_name = 'kinesis-mobile-log-stream'
    shard_count = 1


    try:
        response = kinesis_client.create_stream(
            StreamName=stream_name,
            ShardCount=shard_count
        )
        print(f"Creating Kinesis stream '{stream_name}' with {shard_count} shard(s)...")
        
    except ClientError as e:
        print(f"Error creating stream: {e}")
        
