import sys
import glob, os
import shutil
import random
import json
import boto3
from botocore.exceptions import ClientError
import AWS_S3_helper as a4
from AWS_S3_helper import Bucketmanip

ifunct = Bucketmanip()
listbuckets = ifunct.getallbuckets()

REGION = 'us-west-1'
s3_resource = boto3.resource('s3')

#print ('Number of arguments:', len(sys.argv), 'arguments.')
#print ('Argument List:', str(sys.argv))
param = 3
usage = "user password"
if len(sys.argv) < param:
    print()
    ifunct.printparamerror(param, sys.argv[0], usage)
    quit()
else:
    user = sys.argv[1]
    password = sys.argv[2]
    print("\nThis script checks user, userpasswords against the values saved in user file.")
    print("If match is found the function to list files in user's bucket is called.\n")

#print(user, password)

'''user = 'chicken'
password ='chickpswd'
file_to_upload = "filetoupload.txt"'''

first_bucket_name = ifunct.checkfibucketexists(a4.allb)
second_bucket_name = ifunct.checkfibucketexists(user)

if first_bucket_name is None:
    ifunct.noallusersbucket()
    quit()
elif second_bucket_name is None:
    ifunct.nobucketforauser(user)
    quit()
else:
    print("User bucket found: ",second_bucket_name, "\n")
    check = ifunct.comparepasswords(first_bucket_name,user, password)
    if check is not None:
        filesinb = ifunct.listbucketcontent(second_bucket_name)
        if filesinb:
            for item in filesinb:
                print(item)
            print()
        else:
            print("User bucket is empty. Upload something in there first\n\n")
    else:
        ifunct.passwordontmatch(user)
        quit()
            
            
