import sys
import os
import shutil
import random
import json
import boto3
import uuid
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
s3_connection=s3_resource.meta.client

bucket_prefix = "v-bucket-"
b_name = []
# using uuid to generate random bucket suffix
def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
    return ''.join([bucket_prefix, str(uuid.uuid4())])

# create actual buckets on AWS
def create_bucket(bucket_prefix, s3_connection,current_region='us-west-1'):
    #session = boto3.session.Session()
    #current_region = session.region_name
    bucket_name = create_bucket_name(bucket_prefix)
    bucket_response = s3_connection.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
        'LocationConstraint': current_region})
    #print(bucket_name, current_region)
    return bucket_name, bucket_response


def create_buckets_on_aws(numofbuckets=0):
    for _ in range(numofbuckets):
        try:
            bucket_name, response = create_bucket(bucket_prefix,s3_connection=s3_resource.meta.client)
            b_name.append(bucket_name)
            print(bucket_name, response,"\n")
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print("Already Exists")
            elif e.response['Error']['Code'] == 'InvalidBucketName':
                print("Invalid Bucket Name issue.")
            else:
                print("Unexpected error: %s" % e)


create_buckets_on_aws(1)
print(b_name)
