import sys
import datetime
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from awsglue import DynamicFrame
from awsglue.transforms import ApplyMapping

# ----------- Read Arguments -----------
args = getResolvedOptions(
    sys.argv,
    ['JOB_NAME', 'TempDir', 'STREAM_ARN', 'OUTPUT_PATH']
)

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

stream_arn = args['STREAM_ARN']
output_path_base = args['OUTPUT_PATH']

# ----------- Source: Kinesis Stream -----------
dataframe_kinesis = glueContext.create_data_frame.from_options(
    connection_type="kinesis",
    connection_options={
        "typeOfData": "kinesis",
        "streamARN": stream_arn,
        "classification": "json",
        "startingPosition": "earliest",
        "inferSchema": "true"
    },
    transformation_ctx="dataframe_kinesis"
)

# ----------- Processing Logic -----------
def processBatch(data_frame, batchId):
    if data_frame.count() > 0:
        # Convert to Glue DynamicFrame
        dyf = DynamicFrame.fromDF(data_frame, glueContext, "from_data_frame")

        # Apply schema mapping (update according to your data)
        mapped_dyf = ApplyMapping.apply(
            frame=dyf,
            mappings=[
                ("hour", "string", "hour", "timestamp"),
                ("lat", "string", "lat", "double"),
                ("long", "string", "long", "double"),
                ("signal", "string", "signal", "int"),
                ("network", "string", "network", "string"),
                ("operator", "string", "operator", "string"),
                ("status", "string", "status", "int"),
                ("description", "string", "description", "string"),
                ("speed", "string", "speed", "double"),
                ("satellites", "string", "satellites", "double"),
                ("precission", "string", "precission", "double"),
                ("provider", "string", "provider", "string"),
                ("activity", "string", "activity", "string"),
                ("postal_code", "string", "postal_code", "int"),
            ],
            transformation_ctx="mapped_dyf"
        )

        # Dynamic partition path based on ingestion time
        now = datetime.datetime.now()
        output_path = (
            output_path_base
            + f"/ingest_year={now.year:04d}/ingest_month={now.month:02d}/"
            + f"ingest_day={now.day:02d}/ingest_hour={now.hour:02d}/"
        )

        # Write to S3 in CSV with Snappy compression
        glueContext.write_dynamic_frame.from_options(
            frame=mapped_dyf,
            connection_type="s3",
            format="csv",
            connection_options={"path": output_path, "partitionKeys": []},
            format_options={"compression": "snappy"},
            transformation_ctx="s3sink"
        )

# ----------- Glue Streaming Trigger -----------
glueContext.forEachBatch(
    frame=dataframe_kinesis,
    batch_function=processBatch,
    options={
        "windowSize": "100 seconds",
        "checkpointLocation": args["TempDir"] + "/" + args["JOB_NAME"] + "/checkpoint/"
    }
)

job.commit()
