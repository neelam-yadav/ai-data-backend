import boto3

def ingest_datalake(bucket_name, prefix):
    """
    Fetches data from an S3 data lake.
    :param bucket_name: S3 bucket name.
    :param prefix: S3 prefix for files.
    :return: List of objects from S3.
    """
    s3 = boto3.client('s3')
    objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)["Contents"]
    return [{"source": "datalake", "content": obj, "metadata": {}} for obj in objects]
