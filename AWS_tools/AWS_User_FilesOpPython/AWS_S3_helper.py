import sys
import glob, os
import shutil
import random
import json
import boto3
import uuid
from botocore.exceptions import ClientError
allb = 'allusersb'
s3_resource = boto3.resource('s3')

# using uuid to generate random bucket suffix
def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
    return ''.join([bucket_prefix, str(uuid.uuid4())])

class Bucketmanip():

    REGION = 'us-west-1'
    
    def __init__(self):
        pass

    # 1. list all the bucket on the S3
    def getallbuckets(self):
        try: 
            listbuckets = [bucket.name for bucket in s3_resource.buckets.all()]
            #print(type(listbuckets))
            return listbuckets 
        except ClientError:
            return None

    # 2. list files in bucket
    def listbucketcontent(self,bucket_name):
        allkeys = []
        try:
            s3_resource.meta.client.head_bucket(Bucket=bucket_name)
            bname = s3_resource.Bucket(bucket_name) 
            for file in bname.objects.all ():
                    allkeys.append(file.key)
            return allkeys          
        except ClientError:
            return None
        

    # 3. print file metadata and file body into stdout
    def getobjectinfofrombucket(self, bucket_name,file_name): 
        mlist =[]   
        try:
            fi = s3_resource.Object(bucket_name,file_name)
            mlist = [fi.content_length, fi.last_modified, fi.get()]
            # print ('\nContents of object:' + objectname + ' in bucket:' + bucketname + '=' + str(contents))
            return mlist
        except ClientError:
            return None

    # 4. upload file into bucket  
    def addfiletobucket(self, bucket_name,file_to_upload,region = REGION):
        s3_resource = boto3.resource('s3',region_name=Bucketmanip.REGION) 
        try:
            s3_resource.Bucket(bucket_name).upload_file(Filename=file_to_upload, Key=file_to_upload)
            return ('Added ' + file_to_upload + ' file:' + ' to bucket: ' + bucket_name)
        except (ClientError,FileNotFoundError) as e:
            return e

    # 5. download file from the bucket into your local directory
    def getfilefrombucket(self, bucket_name,key,localfilename,region = REGION):
        s3_resource = boto3.resource('s3',region_name=Bucketmanip.REGION) 
        bucket = s3_resource.Bucket(bucket_name)
        objs = list(bucket.objects.filter(Prefix=key))

        if not objs:
            return None
        elif os.path.isdir(localfilename):
            return (localfilename  + 'is directory:' + localfilename + ' no action taken')    
        elif os.path.isfile(localfilename):
            savefilename = ''.join([str(uuid.uuid4().hex[:6]), localfilename + '.bak' ])
            #result = ('saving existing file:' + localfilename + ' to:' + savefilename)
            shutil.move(localfilename,savefilename)
            s3_resource = boto3.resource('s3',region_name=Bucketmanip.REGION)
            bucket=s3_resource.Bucket(bucket_name)
            bucket.download_file(key,localfilename)
            return (' from key:' + key + ' in bucket:' + bucket_name + ' downloaded into:' + localfilename)
        
        else:
           
            bucket=s3_resource.Bucket(bucket_name)
            bucket.download_file(key,localfilename)
            return (' from key:' + key + ' in bucket:' + bucket_name + ' downloaded into:' + localfilename)

    # 6. write key/value into bucket using stdin
    def writestringintobucket( self, bucket_name,keyname,stringdata,region = REGION):   
            bucket=s3_resource.Bucket(bucket_name)
            stringasbinary = stringdata.encode() 
            try:
                bucket.put_object(Key=keyname,Body=stringasbinary)
                #bucket.put_object_acl(Key=keyname,Body=stringasbinary)
                return("Done!") #to do investigate the signals
            except ClientError as e:
                return(e)

    # 7. print value content from the bucket into stdout
    def readstringfromobject(self,bucket_name,keyname,region = REGION): 
        bucket=s3_resource.Bucket(bucket_name)
        key=bucket.Object(keyname)
        resp=key.get() 
        if resp != None:
            strn=resp["Body"].read() 
        else:
            strn='No Data' 
        return strn

    # 8. crete a bucket
    def create_bucket(self, bucket_name, region = REGION):
        try:
            bucket_response = s3_resource.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                'LocationConstraint': region})
            #print(bucket_name, current_region)
            return (bucket_name, bucket_response)
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print("Bucket already exists")
            elif e.response['Error']['Code'] == 'InvalidBucketName':
                print("Invalid Bucket Name issue.")
            else:
                print("Unexpected error: %s" % e)

    # 9. cp objects between buckets
    def copy_to_bucket(self,bucket_from_name, bucket_to_name, file_name):      
        try:
            copy_source = {
            'Bucket': bucket_from_name,
            'Key': file_name
            }
            s3_resource.Object(bucket_to_name, file_name).copy(copy_source)  
            return ("Copied " + file_name + " from " + bucket_from_name + " to " + bucket_to_name)
        except ClientError:
            return None

    # 10. parse bucket name and find user name. My bucket prefix is user name plus dash.
    def parce_bucket_name(self):
        curent_users_b =[]
        listbuckets = self.getallbuckets()        
        userb = [x for x in listbuckets if listbuckets is not None] 
        if userb:
            for i in userb:
                ub = i.split('-',1)[0]
                curent_users_b.append(ub)
            return (curent_users_b)
        else:
            return None

    # 11. delete file from s3 bucket
    def delete_file(self,bucket_name, file_name, region = REGION):
        bucket = s3_resource.Bucket(bucket_name)
        response = bucket.delete_objects(
            Delete={
                'Objects': [
                    {
                        'Key': file_name
                    }
                ]
            }
        )
        return response

    # 12 Check if single bucket exists in S3:
    def checkfibucketexists(self, bname, region=REGION):
        listbuckets = self.getallbuckets()
        bname = bname+'-'
        if len(listbuckets) > 0:
            try:
                name = [x for x in listbuckets if bname in x]
                if len(name)>0:
                    bucket_name = name[0]
                    return bucket_name
                else:
                    return None
            except ClientError:
                return None
    
    # 13 print no buckets message
    def nobuckets(self, user, password):
        print("No available buckets on S3. Run python CreateUser.py ", user, password, "email")

    # 14 compare passwords 
    def comparepasswords(self, name, user, password, region=REGION): 
        reed_user_file_result = self.readstringfromobject(name, user)
        upass = reed_user_file_result.decode('utf-8')
        upass = upass.split(' ', 1)[0]
        if password == upass:
            return password
        else:
            return None
    # 15 print there is no alluser bucket
    def noallusersbucket(self):
        print("There is no All Users bucket! Exiting...")

    # 16 print there is no bucket for a user
    def nobucketforauser(self, user):
        print("There is no bucket for ",user,"... Run CreateUser.py first Exiting...")

    # 17 print password does not mach
    def passwordontmatch(self,user):
        print("Pasword does not match for ", user ,"! Exiting....")

    # 18  print param error
    def printparamerror(self,numparam, scriptname, usage):
         print("Invalid number of arguments, must be equal to ", numparam-1)
         print("Usage: ", scriptname, usage)
         print("Exiting ", scriptname, " plese try again with correct parameters!")
         

def main():
    pass
              
if __name__ == '__main__':
    main()               