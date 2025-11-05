import csv, json, time, boto3

def producer():

    STREAM_NAME = "kinesis-mobile-log-stream"
    CSV_PATH = "mobile-logs-generated.csv"  
    SLEEP = 0.05

    kinesis = boto3.client("kinesis", region_name="us-east-1")

    with open(CSV_PATH, 'r') as f:

        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            data = json.dumps(row)
            kinesis.put_record(StreamName=STREAM_NAME, Data=data.encode('utf-8'), PartitionKey=str(i%10))
            if i % 100 == 0:
                print("sent", i)
            time.sleep(SLEEP)
            #print(data)

