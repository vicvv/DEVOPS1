import os, sys, time, timeit, inspect, subprocess
import boto3
import botocore
import subprocess
import paramiko
import urllib.request
import urllib.error
from scp import SCPClient
from botocore.exceptions import ClientError
from AWS_9_helper import Insclass as Insclass

# below method prings usage
def usage():
    print('usage: python AWS_9_Tomcat.py securityGroup sshKeyName sshKeyFolder region securityGroup1 sshKeyName1 sshKeyFolder1, region1')

# below method verifies if all input parameters make sence or exists
def verifyparams(mycl,securitygroup,securitykey,keylocation,region):
    fullpath = os.path.join(keylocation, securitykey) + '.pem'
    securitygroupid = mycl.findsecgrid(securitygroup, region)

    if not securitygroup or not region:
        print("Invalid input, provide name for security group and/or region")
        usage()
        return None 

    elif os.path.isdir(keylocation) == False:
        print('cannot find key location folder:' + keylocation)
        usage()
        return None 

    elif os.path.exists(fullpath) == False:
        print('cannot find keyfile:' + fullpath)
        print('current folder is:' + os.getcwd())
        usage()
        return None

   # this check confirms if security groupid is exists for provided group name
   # if we cant aquire security group id than there is no reason to continue the script
    elif securitygroupid is None:
        print("Cant find security group id for provided group name ", securitygroup)
        return None

    else:
        print("Security Group Id found:",securitygroupid)
        return 'OK'

# method below is called by main function and is accessing AWS_HW9_helper.py script to complete the process
def myinstmanip(mycl,securitygroup,ami_instance,securitykey,region,count):   
    (instid, dns_name, ip_address) = mycl.startinstance(securitygroup,ami_instance,securitykey,region,count)
    mycl.start_tomcat(instid, dns_name, ip_address, securitykey, region)
    mycl.movemyapp(instid,ip_address,securitykey)
    
    exists = os.path.isfile("deleteme.txt")
    if exists:
        os.remove("deleteme.txt")
        filefunct(mycl)
    else:
        filefunct(mycl)
            
# method below exists to create a file with instance id and region.
# the data in the file is used to delete the instance by running delete_instance.py             
def filefunct(mycl):
    for i in range(len(mycl.instanceIds)):
        with open("deleteme.txt", 'a+') as fh:
            fh.write(mycl.instanceIds[i] + ' ' + mycl.regions[i] + '\n')
            # if it is require to delete the instance immediatelly please uncomment line below
            # mycl.delete_instance(mycl.instanceIds[i],mycl.regions[i])

# below variable are for debug purpouse only and must be comented out if script to run in production mode
# if you wish to test the script in debug mode please replace the values for parameters below.
# for us-west-1
ami_instance = 'ami-824c4ee2'
securitygroup = 'awsclass01a'
securitykey = ''
keylocation = ''
region = 'us-west-1'


# for us-east-1
ami_instance1 =  'ami-0080e4c5bc078760e'
securitygroup1 = 'awclass-us-east-1'
securitykey1 = ''
keylocation1 = '/'
region1 = 'us-east-1'

# lines below are checking the number of imput paramters
# uncomment below lines if you need to run the file in command line mode


# if len(sys.argv) != 9:
#    usage()
#    quit()

# else:
#     securitygroup = sys.argv[1]
#     securitykey = sys.argv[2]
#     keylocation = sys.argv[3]
#     region = sys.argv[4]
#     securitygroup1 = sys.argv[5]
#     securitykey1 = sys.argv[6]
#     keylocation1 = sys.argv[7]
#     region1 = sys.argv[8]


# number of instances to start determined by var count
count = 1 

print('Python version:' + ".".join(map(str, sys.version_info[:3])))
print('Boto3 version:' + boto3.__version__)
print('Paramiko version:' +  paramiko.__version__)

# instantiating the class
mycl = Insclass()

# verifying if all suplied parameters make sence
res = verifyparams(mycl, securitygroup,securitykey,keylocation,region)
res1 = verifyparams(mycl, securitygroup1,securitykey1,keylocation1,region1)

if res is None or res1 is None:
    print("Invalid arguments, try again")
    quit()

myinstmanip(mycl,securitygroup,ami_instance,securitykey,region,count)
myinstmanip(mycl,securitygroup1,ami_instance1,securitykey1,region1,count)

