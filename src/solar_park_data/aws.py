import boto3
from mypy_boto3_s3 import S3Client


def s3_client(access_key_id: str, secret_access_key: str) -> S3Client:
    return boto3.client(
        "s3", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key
    )
