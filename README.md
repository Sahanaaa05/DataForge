## Telecom Signal

## Stream

### Data Forge


##### Team

##### Members

- Ijaz Ahmad S
- Kavya Bhatta S
- Rakesh Kumar
- Sahana J Upadhyaya


Problem Statement

- Telecom companies generate huge volumes of mobile-signal data every day.
- Delayed or manual analysis slows down issue detection and response.
- Need a real-time solution to monitor and analyse network health instantly.

Objective

- Build a real-time analytics pipeline using AWS Kinesis, Glue, Athena, and CloudWatch.
- Enable continuous tracking of key metrics like signal strength, GPS precision, and network status.

Use Case

- Simulate mobile log data (CSV) as live stream via Kinesis.
- Perform ETL and cleaning using AWS Glue.
- Store curated data in S3 and query insights with Athena.
- Key Metrics:
    - Avg. Signal Strength per Region
    - GPS Accuracy per Postal Area and Operator
    - Network activity (Still, Tilting, Unknown, On_Foot, In_Vehicle)


##### Input Data Overview

- Schema & Sample
    - Dataset : mobile_logs
    - Format –csv
    - Streaming Data

hour lat long signal network operator status description speed satellites precision provider activity
00:36:07.000 9.7028 -16.9857 15 DTAC JAZZTEL 0 STATE_IN_SERVICE 35.6 5.6 144.1fused STILL
00:36:08.000 3.68379 -2.76099 22 movistar DTAC 0 STATE_IN_SERVICE 128.9 6.3 14.6fused STILL
00:36:09.000 28.02161 -3.30627 16 orange RACC 0 STATE_IN_SERVICE 134.9 2.6 126.4fused UNKNOWN
00:36:10.000 16.51063 -9.35435 6 orange vodafoneES 0 STATE_IN_SERVICE 45.3 11 139.9fused UNKNOWN
00:36:11.000 16.803 -12.9745 6 vodafone Orange 0 STATE_IN_SERVICE 123 14.7 28 gps IN_VEHICLE


##### High-Level Architecture


##### Tools & Services Used:

Service Purpose
Central data lake (stores raw, processed, scripts,
Amazon S3 checkpoints, and query outputs).

Real-time ingestion of mobile log data (acts as the
Amazon Kinesis Data Stream streaming data source).

Performs ETL processing (Spark Streaming job
AWS Glue reads from Kinesis, writes to S3 in Parquet).

Provides roles and permissions for Glue, Kinesis,
AWS IAM and S3 access control.

Serverless query engine to analyze processed data
Amazon Athena stored in S3 using SQL.

Monitors Glue job execution and logs for
Amazon CloudWatch troubleshooting.


##### Detailed Pipeline Flow


Data Ingestion

- Python Data Ingestion
Script
    - Simulates real-time
       telecom data from CSV.
    - Converts each row to JSON
       and sends it to Kinesis
       Data Stream.


##### S3 Bucket Setup


###### Kinesis Data Stream

```
Serverless Amazon Web Services (AWS) service
for processing and analyzing real-time streaming
data at scale.
```

#### AWS Glue Job


##### AWS Glue Streaming ETL Job (Status)


##### KPI’s

- Average signal by operator • Average signal by postal code


##### KPI’s

- Average signal by operator and postal code • Average GPS precision by provider


###### KPI’s

Activity Count


##### Business Output

- Real-time data availability : Incoming mobile
    log data instantly processed and stored in S3.
- Clean & structured datasets : JSON stream
    transformed into timestamped, analytics-
    ready CSV files.
- Faster insights : Teams can query live data
    using Amazon Athena without manual ETL
    steps.
- Scalable foundation : The pipeline can easily
    integrate new data sources or analytics
    dashboards (QuickSight, Power BI).


##### Key

##### Learnings

1. AWS Data Pipeline Design : Learned how to build a
    real-time data pipeline connecting Kinesis Data
    Stream → AWS Glue → S3 → Athena for end-to-end
    data processing.
2. Spark Structured Streaming : Gained hands-on
    experience with reading continuous streams and
    writing results.
3. Schema Handling & Data Transformation : Practiced
    defining JSON schemas, parsing dynamic data, and
    transforming raw data into structured CSV output.
4. Offline Testing & Local Simulation : Developed a local
    test setup using Docker + Spark to simulate
    streaming with JSON files before deploying to AWS.
5. AWS Cloud Integration : Explored Glue Catalog,
    Athena, and S3 as a seamless ecosystem for data
    storage, querying, and analytics.


##### Future Scope

Real-Time Analytics Dashboard

```
Integrate with Amazon QuickSight or
Grafana for live visualization of streaming
data.
```
Data Quality & Validation Layer Add AWS Lambda or Glue triggers to validate and cleanse data before storage.

```
Scalable Multi-Stream
Integration
```
```
Extend the pipeline to handle multiple
Kinesis streams for different data sources
or applications.
```

# Thank you


