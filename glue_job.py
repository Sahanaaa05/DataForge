import boto3


def glue_job():
    # Initialize Glue client
    glue = boto3.client('glue')

    # Define parameters
    job_name = 'DataForgeGlueJob1'
    role_name = 'glue-Stream-Execution-Role'
    script_s3_path = 's3://data-forge-bkt1/scripts/script'
    dependent_jars = 's3://data-forge-bkt1/PathToJar/spark-streaming-kinesis-asl_2.12-3.5.5.jar'

    try:
        response = glue.create_job(
            Name=job_name,
            Role=role_name,
            ExecutionProperty={
                'MaxConcurrentRuns': 1
            },
            Command={
                'Name': 'glueetl',
                'ScriptLocation': script_s3_path,
                'PythonVersion': '3'
            },
            DefaultArguments={
                '--extra-jars': dependent_jars
            },
            GlueVersion='5.0',
            Description='Streaming Glue job for DataForge project',
            Tags={
                'Project': 'DataForge',
                'Type': 'StreamingJob'
            }
        )
        
        print(f"Glue job '{job_name}' created successfully!")
        print("Response:", response)

    except glue.exceptions.AlreadyExistsException:
        print(f"Glue job '{job_name}' already exists.")

    except Exception as e:
        print("Error creating Glue job:", str(e))
