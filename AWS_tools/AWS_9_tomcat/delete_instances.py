import os
import time
import boto3
import glob
from botocore.exceptions import ClientError
cwd = os.getcwd()

with open('deleteme.txt') as fo:   
    for line in fo:
        instanceid, region = line.split()
        ec2 = boto3.client('ec2', region_name=region)
        response=ec2.terminate_instances(InstanceIds=(instanceid,)) #JSON is returned
        print ('The following instances have been queued for termination: ', instanceid, response)


    