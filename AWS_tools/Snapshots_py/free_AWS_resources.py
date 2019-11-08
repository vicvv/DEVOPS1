#********************************
#Step 07: ec2run_Part5.py
# cleanup aws resources
#********************************

import os
import time
import boto3
import glob
from botocore.exceptions import ClientError
cwd = os.getcwd()

region='us-west-1'
ec2 = boto3.client('ec2', region_name=region)


################################################
#delete ec2 instance
for filename in glob.glob(os.path.join(cwd, 'instidfile*')):
    if os.path.exists(filename) == False:
        print(filename + " does not exist")
        quit()
    else:
        fileobj = open(filename, 'r')
        instidP = fileobj.read()
        instid = instidP.strip().strip('\n\r')
        fileobj.close()
        os.remove(filename)
    #terminate ec2 instance
    try: 
        print('will delete instance-id:' + instid)
        ec2.terminate_instances(InstanceIds=[instid])

        time.sleep(15)
        bIsRunning = True
        while bIsRunning == True:
            rz=ec2.describe_instance_status(InstanceIds=[instid])
            #call can return before all data is available
            if not bool(rz):
                time.sleep(15)
                continue
            if len(rz["InstanceStatuses"]) == 0:
                break

            inststate=rz["InstanceStatuses"][0]["InstanceState"]
            #print(json.dumps(inststate,indent=2,separators=(',',':')))
            state=inststate["Name"]
            if state == 'terminated' or state == 'shutting-down' or  state == 'stopping':
                bIsRunning = False
            
            print('waiting for ec2 instance to stop')
            time.sleep(30)

        print("EC2 instance is termniated")
    except ClientError as e:
        print(e)
        pass

################################################
#delete volume

for filename in glob.glob(os.path.join(cwd, 'volumeidfile*')):
    if os.path.exists(filename) == False:
        print(filename + " does not exist")
        quit()
    try:
        fileobj = open(filename, 'r')
        volume_idP = fileobj.read()
        volume_id = volume_idP.strip().strip('\n\r')
        print('will delete volume-id:' + volume_id)
        ec2.delete_volume(VolumeId=volume_id)
        os.remove(filename)
    except ClientError as e:
        print(e)
        pass

################################################
#delete snapshot
for filename in glob.glob(os.path.join(cwd, 'snapshotid*')):
    if os.path.exists(filename) == False:
        print(filename + " does not exist")
        quit()
    try:
        fileobj = open(filename, 'r')
        snapidP = fileobj.read()
        snapid = snapidP.strip().strip('\n\r')
        fileobj.close()
        print("will delete snapshot-id:" + snapid)
        ec2.delete_snapshot(SnapshotId=snapid)
        os.remove(filename)
    except ClientError as e:
        print(e)
        pass

        print('***** all done *****')
        exit(0)

