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
usage = "user password file_to_download"

if len(sys.argv) < param:
    print()
    ifunct.printparamerror(param, sys.argv[0], usage)
    quit()
else:
    user = sys.argv[1]
    password = sys.argv[2]
    file_to_download = sys.argv[3]
    print("\nThis script checks user, userpasswords against the values saved in user file.")
    print("If match is found the function to download file: ", file_to_download, "is called.")
    print("If", file_to_download, "exists in local directory it will be renamed to *.bak before\
 downloading \n")

#print(user, password, file_to_download)

'''user = 'chicken'
password ='chickpsw'
file_to_download = "filetoupload.txt"'''

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
        copyresult = ifunct.copy_to_bucket(first_bucket_name, second_bucket_name, user)
        print(copyresult, "because password matches")
        print("Now downloading file: ",file_to_download, "from ",  second_bucket_name, \
            " into local directory ", cwd, "...\n")
        download_result = ifunct.getfilefrombucket(second_bucket_name,file_to_download,file_to_download)          
        print(download_result , "\n")
        os.system('ls -l')
        #os.system('ls -l *.bak')
        #os.system('ls -l ${file_to_download}')
    else:
        ifunct.passwordontmatch(user)
        quit()
            














'''available_users_buckets = ifunct.parce_bucket_name()
print(available_users_buckets)

if available_users_buckets is not None:
    if a4.allb not in available_users_buckets:
        print("There is no All bucket users. Need to run CreateUser.py first")
    else:
        print("Bucket for all users is available")
        name = [x for x in listbuckets if a4.allb in x]
        first_bucket_name = name[0]

    if user not in available_users_buckets:
        print(user, " does not have a bucket. Need to CreateUser.py first")
        quit()
       
    else:
        print(user, " bucket is availabe")
        ubname = [x for x in listbuckets if user in x]
        print(ubname)
        for item in ubname:
            ub = item.split('-',1)[0]
            if ub == user:
                second_bucket_name = item
            else:
                pass
        print(second_bucket_name)
        copyresult = ifunct.copy_to_bucket(first_bucket_name, second_bucket_name, user)
        print(copyresult)

        reed_user_file_result = ifunct.readstringfromobject(second_bucket_name, user)
        upass = reed_user_file_result.decode('utf-8')
        upass = upass.split(' ', 1)[0]
        print(upass)
        if password == upass:
            print("downloading file...")
            download_result = ifunct.getfilefrombucket(second_bucket_name,file_to_download,file_to_download)          
            print(download_result)
        else:
            ifunct.delete_file(second_bucket_name, user)
            print("Invalid password")
            quit()
        
        
else:
    ifunct.nobuckets(user, password)
    
'''