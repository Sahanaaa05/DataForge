import boto3
import json
from botocore.exceptions import ClientError

# Initialize the IAM client
iam = boto3.client('iam')

# Step 3 — Create IAM Role for Glue
role_name = 'sig-glue-Stream-Execution-Role'

# Trust policy document for AWS Glue
assume_role_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "glue.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }
    ]
}

# List of managed policies to attach
policies = [
    "arn:aws:iam::aws:policy/AmazonS3FullAccess",
    "arn:aws:iam::aws:policy/AmazonKinesisReadOnlyAccess",
    "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
]

try:
    print(f" Creating IAM Role: {role_name} ...")
    # Create the Glue execution role
    create_role_response = iam.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(assume_role_policy),
        Description="IAM Role for AWS Glue to read from Kinesis and write to S3",
        Tags=[
            {"Key": "Service", "Value": "Glue"},
            {"Key": "Purpose", "Value": "StreamExecution"}
        ]
    )
    print(" Role created successfully!\n")

    # Attach each required policy
    for policy_arn in policies:
        print(f" Attaching policy: {policy_arn}")
        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )

    print("\n All policies attached successfully!")
    print(f" IAM Role '{role_name}' is ready for use with AWS Glue.")

except ClientError as e:
    print(f" Error: {e.response['Error']['Message']}")
