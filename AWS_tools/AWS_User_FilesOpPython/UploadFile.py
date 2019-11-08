import sys
import glob, os
import shutil
import json
import boto3
from botocore.exceptions import ClientError
import AWS_S3_helper as a4
from AWS_S3_helper import Bucketmanip
cwd = os.getcwd() 
ifunct = Bucketmanip()
listbuckets = ifunct.getallbuckets()

REGION = 'us-west-1'
s3_resource = boto3.resource('s3')

param = 4
usage = "user password file_to_upload"
if len(sys.argv) < param:
    ifunct.printparamerror(param, sys.argv[0], usage)
    quit()
else:
    user = sys.argv[1]
    password = sys.argv[2]
    fp=sys.argv[3]
    print("This script checks user, userpasswords against the values saved in user file.")
    print("If match is found the function to upload file: ", fp, "is called.")
    print("This script does not check if file to upload is already in S3, so the file is overriden.")
    print("If your input path or file has spaces provide backslash before the space in path or file name.")
    print(fp)
#print(user, password, file_to_upload)

'''user = 'mycat'
password ='mycatpass'
fp = "/Users/vicky/Desktop/AWS_Class/AWS_Homeworks/file to upload.txt"'''

(mypath,file_to_upload) = os.path.split(fp)
print(mypath,file_to_upload)
#copyfile(fp, cwd)
shutil.copy(fp, cwd)
first_bucket_name = ifunct.checkfibucketexists(a4.allb)
second_bucket_name = ifunct.checkfibucketexists(user)

if first_bucket_name is None:
    ifunct.noallusersbucket()
    quit()
elif second_bucket_name is None:
    ifunct.nobucketforauser(user)
    quit()
else:
    print(first_bucket_name, second_bucket_name)
    check = ifunct.comparepasswords(first_bucket_name,user, password)
    if check is not None:       
        #copyresult = ifunct.copy_to_bucket(first_bucket_name, second_bucket_name, user)
        #print(copyresult, "because password matches")
        print("Now uploading file into user bucket...")
        upload_result = ifunct.addfiletobucket(second_bucket_name,file_to_upload)           
        print(upload_result)
    else:
        ifunct.passwordontmatch(user)
        quit()
            

