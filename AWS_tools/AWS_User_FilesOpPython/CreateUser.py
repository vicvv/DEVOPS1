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

param = 4
usage = "username user_password user_email"
if len(sys.argv) < 4:
    ifunct.printparamerror(param, sys.argv[0], usage)
    quit()
else:
    user = sys.argv[1]
    # dont allaw dash in user name because I am going to use dash in future parsing
    if "-" in user: print("User name can't have a dash! Quiting the ", sys.argv[0]); quit()
    password = sys.argv[2]
    email = sys.argv[3]
    print("\nThis script checks for All users bucket and for user bucket.\n\
If buckets not found they are created and key", user,"with userid, password and \
email as values is cureated under All users bucket.\n")

# this is for testing, do not delete
'''user = "chicken"
password = "snakep"
email = "snake@ratle.com"'''

def create_named_bucket(*params):
    if len(params) == 1:
        print('Bucket for all users is not found.')
        bucket_name = a4.create_bucket_name(params[0] + '-')
        print("Creating ", bucket_name)
        try:
            (bucket_name, bucket_response) = ifunct.create_bucket(bucket_name)
            return(bucket_name, bucket_response)
        except (ClientError, TypeError) as e :
            print(e)
    elif len(params) == 4:
        print(params[0], params[1], params[2],params[3])

        #(user, password, email, bucket_name)
        user_bucket_name = a4.create_bucket_name(params[0]+ "-")
        try:
            (user_bucket_name, bucket_response) = ifunct.create_bucket(user_bucket_name)       
            myres = ifunct.writestringintobucket(params[3],params[0],params[1] + " " + params[2])
            if(myres):
                print(myres)
                print("The following file was created in ", params[3], ": ", user)
                #print(user_bucket_name, bucket_response)
        except (ClientError, TypeError) as e:
            print(e)

first_bucket_name = ifunct.checkfibucketexists(a4.allb)
second_bucket_name = ifunct.checkfibucketexists(user)

if first_bucket_name is None:
    (first_bucket_name, bucket_response) = create_named_bucket(a4.allb)
    print(first_bucket_name, "is created.")
if second_bucket_name is None:
    create_named_bucket(user, password, email, first_bucket_name)
else:
    print(first_bucket_name, second_bucket_name)
    # owerride the user credentials. This will happen every time for each existing users in CreateUser.py
    # this was a requirement
    myres = ifunct.writestringintobucket(first_bucket_name, user, password + " " ,email)
    print(myres)






    


