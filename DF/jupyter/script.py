import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType
from pyspark.sql.functions import col, from_json, to_timestamp

# ---- Glue job args ----
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# ---- Config ----
region = "us-east-1"
stream_name = "kinesis-mobile-log-stream"
s3_checkpoint = "s3://data-forge-bkt1/checkpoint/"
s3_output_main = "s3://data-forge-bkt1/processed/main/"
s3_output_agg_operator = "s3://data-forge-bkt1/processed/avg_signal_operator/"
s3_output_agg_postal = "s3://data-forge-bkt1/processed/avg_signal_postal/"
s3_output_agg_combo = "s3://data-forge-bkt1/processed/avg_signal_operator_postal/"
s3_output_agg_gps = "s3://data-forge-bkt1/processed/avg_precision_gps/"
s3_output_activity = "s3://data-forge-bkt1/processed/activity_count/"

# ---- Read from Kinesis ----
raw_df = (
    spark.readStream
        .format("aws-kinesis")
        .option("kinesis.region", region)
        .option("kinesis.streamName", stream_name)
        .option("kinesis.consumerType", "GetRecords")
        .option("kinesis.startingposition", "LATEST")
        .option("kinesis.endpointUrl", f"https://kinesis.{region}.amazonaws.com")
        .load()
)

print("Streaming source initialized:", raw_df.isStreaming)

# ---- Parse JSON payload ----
df_json = raw_df.selectExpr("CAST(data AS STRING) as json_data")

# Schema definition
schema = StructType([
    StructField("hour", StringType(), True),
    StructField("lat", StringType(), True),
    StructField("long", StringType(), True),
    StructField("signal", StringType(), True),
    StructField("network", StringType(), True),
    StructField("operator", StringType(), True),
    StructField("status", StringType(), True),
    StructField("description", StringType(), True),
    StructField("speed", StringType(), True),
    StructField("satellites", StringType(), True),
    StructField("precision", StringType(), True),
    StructField("provider", StringType(), True),
    StructField("activity", StringType(), True),
    StructField("postal_code", StringType(), True)
])

parsed_df = df_json.select(from_json(col("json_data"), schema).alias("data")).select("data.*")

# ---- Cast to correct data types ----
df_casted = (
    parsed_df
    .withColumn("hour", to_timestamp(col("hour")))
    .withColumn("lat", col("lat").cast(DoubleType()))
    .withColumn("long", col("long").cast(DoubleType()))
    .withColumn("signal", col("signal").cast(IntegerType()))
    .withColumn("status", col("status").cast(IntegerType()))
    .withColumn("speed", col("speed").cast(DoubleType()))
    .withColumn("satellites", col("satellites").cast(DoubleType()))
    .withColumn("precision", col("precision").cast(DoubleType()))
    .withColumn("postal_code", col("postal_code").cast(IntegerType()))
)

# ---- Write main cleaned data to S3 ----
main_query = (
    df_casted.writeStream
        .format("csv")
        .option("path", s3_output_main)
        .option("checkpointLocation", s3_checkpoint + "main/")
        .option("header", "true")
        .outputMode("append")
        .start()
)

def write_aggregates_to_s3(batch_df, batch_id):
    # Average signal by operator
    avg_by_operator = (
        batch_df.groupBy("operator")
        .agg(F.avg("signal").alias("Avg_Signal"))
    )
    avg_by_operator.write.mode("overwrite").csv(s3_output_agg_operator)

    # Average signal by postal code
    avg_by_postal = (
        batch_df.groupBy("postal_code")
        .agg(F.avg("signal").alias("Avg_Signal"))
    )
    avg_by_postal.write.mode("overwrite").csv(s3_output_agg_postal)

    # Average GPS precision by provider = 'gps'
    avg_gps = (
        batch_df.filter(col("provider") == "gps")
        .groupBy("operator")
        .agg(F.avg("precision").alias("Avg_Precision"))
    )
    avg_gps.write.mode("overwrite").csv(s3_output_agg_gps )

    # Activity counts
    activity_count = (
        batch_df.groupBy("activity")
        .agg(F.count("*").alias("Activity_Count"))
    )
    activity_count.write.mode("overwrite").csv(s3_output_activity)

# Attach the foreachBatch writer
query = (
    df_casted.writeStream
        .foreachBatch(write_aggregates_to_s3)
        .option("checkpointLocation", "s3://data-forge-bkt1/checkpoint/foreachbatch/")
        .start()
)


print("Streaming Glue job started — transformations running...")

# ---- Await all queries ----
spark.streams.awaitAnyTermination()
job.commit()
