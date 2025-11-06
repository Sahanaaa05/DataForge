import json
import boto3
from botocore.exceptions import ClientError


def iam_role():
    # Initializing IAM client
    iam_client = boto3.client('iam')


    role_name = 'glue-Stream-Execution-Role'

    # Assume role trust policy for Glue
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "glue.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

    # Managed policies to attach
    managed_policies = [
        'arn:aws:iam::aws:policy/AmazonS3FullAccess',
        'arn:aws:iam::aws:policy/AmazonKinesisReadOnlyAccess',
        'arn:aws:iam::aws:policy/CloudWatchLogsFullAccess',
        'arn:aws:iam::aws:policy/AWSGlueConsoleFullAccess'
    ]

    # 1. Create the IAM Role
    try:
        response = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='IAM role for AWS Glue to read Kinesis, write to S3, and log to CloudWatch'
        )
        print(f"Role '{role_name}' created successfully.")
    except ClientError as e:
        print(f"Error creating role: {e}")
        

    # 2. Attach managed policies
    for policy_arn in managed_policies:
        try:
            iam_client.attach_role_policy(
                RoleName=role_name,
                PolicyArn=policy_arn
            )
            print(f"Attached policy: {policy_arn}")
        except ClientError as e:
            print(f"Error attaching policy {policy_arn}: {e}")
