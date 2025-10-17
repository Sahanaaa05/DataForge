import boto3

# Create Kinesis client
kinesis_client = boto3.client('kinesis')

# Define stream parameters
stream_name = 'sig-mobile-log-stream'
shard_count = 1

# Create the data stream
response = kinesis_client.create_stream(
    StreamName=stream_name,
    ShardCount=shard_count
)

# Print the response
print("Stream creation initiated:", response)
