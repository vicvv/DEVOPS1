import sys
import glob, os
import shutil
import json
import boto3
from botocore.exceptions import ClientError
import AWS_S3_helper as a4
from AWS_S3_helper import Bucketmanip

ifunct = Bucketmanip()
listbuckets = ifunct.getallbuckets()

REGION = 'us-west-1'
s3_resource = boto3.resource('s3')

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

param = 4
usage = "user password file_to_delete"
if len(sys.argv) < 4:
    ifunct.printparamerror(param, sys.argv[0], usage)
    quit()
else:
    user = sys.argv[1]
    password = sys.argv[2]
    file_to_delete  = sys.argv[3]
    print("\nThis script checks user, userpasswords against the values saved in user file.")
    print("If match is found the function to delete file: ", file_to_delete, "is called.\n")

#print(user, password, file_to_delete )

'''user = 'chicken'
password ='chickpsw'
file_to_delete = "filetoupload.txt"'''

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
        # i cp user credentials file into user bucket because it was a requrement.    
        copyresult = ifunct.copy_to_bucket(first_bucket_name, second_bucket_name, user)
        print(copyresult, "because password matches\n")
        print("Now deliting file from ", user , "bucket", second_bucket_name)
        '''The xpected behavior for S3. When you delete a nonexistent key, 
        either individually or in a bulk delete operation, any keys that don't exist 
        are treated as deleted keys and no error is returned.'''
        delete_result = ifunct.delete_file(second_bucket_name, file_to_delete)
        print("\n",delete_result)
    else:
        ifunct.passwordontmatch(user)
        quit()
            

