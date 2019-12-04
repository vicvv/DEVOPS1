#*************************
# EC2 helper file
#*************************

import os
import time
import sys
import boto3
import botocore
import botocore.exceptions
from botocore.exceptions import ClientError
import json
import random
import paramiko


class Createinstance:

    # NOTE: you will have  to change the parameters values below
    # class variables
    amiid='ami-824c4ee2'
    instance_type='t2.micro'
    keypair_name=''
    security_group_name=''
    cidr='0.0.0.0/0'
    tag='myinst01'
    user_data=None
    region='us-west-1'
    ec2=boto3.client('ec2',region_name=region)

    def __init__(self):
        pass

    @classmethod
    def launch_instance(cls):        
        # Create a connection to EC2 service and get vpc connection    
        # get the 1st vpc and 1st subnet
        resp=cls.ec2.describe_vpcs()
        vpcidtouse=resp['Vpcs'][0]['VpcId']
        subnetlist=cls.ec2.describe_subnets(Filters=[ {'Name': 'vpc-id', 'Values': [vpcidtouse]} ])
        subnetid = subnetlist['Subnets'][0]['SubnetId']

        # Check to see if specified security group already exists.
        # If we get an InvalidGroup.NotFound error back from EC2,
        # it means that it doesn't exist and we need to create it.
        secgrpname = cls.security_group_name
        bcreatedsecgrp = False
        try:
            secgrpfilter = [
                {
                    'Name':'group-name', 'Values':[secgrpname]
                }
            ]
            secgroups = cls.ec2.describe_security_groups(
                Filters=secgrpfilter
            )
            if secgroups['SecurityGroups']:
                secgrptouse = secgroups["SecurityGroups"][0]
                secgrpid = secgrptouse['GroupId']
            else:
                secgrptouse = cls.ec2.create_security_group(
                    GroupName=secgrpname,Description='aws class open ssh,http,https',
                    VpcId=vpcidtouse)
                secgrpid = secgrptouse['GroupId']
                bcreatedsecgrp = True
        except ClientError as e:
            print("%s " % e.response['Error']['Code'])
            raise

        if (bcreatedsecgrp == True):
            # Add a rule to the security group to authorize ssh traffic
            # on the specified port.
            #open ports 22, 80, 443, 
            portlist = [22, 80, 443]
            for port in portlist:
                try:
                    cls.ec2.authorize_security_group_ingress(
                        CidrIp='0.0.0.0/0', FromPort=port,GroupId=secgrpid,
                        IpProtocol='tcp', ToPort=port)
                except:
                    print("error opening port:" +  str(port))
                    exit()

        try:
            secgrpidlist=[secgrpid]
            numinstances = 1
            resp = cls.ec2.run_instances(ImageId=cls.amiid,  InstanceType=cls.instance_type,
                KeyName=cls.keypair_name,SecurityGroupIds=secgrpidlist,
                SubnetId=subnetid,MaxCount=numinstances, MinCount=numinstances)
        except:
            print("exception:", sys.exc_info()[0])
            raise

        # The instance has been launched but it's not yet up and
        # running.  Let's wait for it's state to change to 'running'.
        # althouth the instance is in running state it might be still in initialization 
        # if an instance in init state but for some reason is also running
        # the snapshot will not be taken properly and that is why I put sleep 120/240 here
        time.sleep(120)
        print('waiting for instance')
        inst=resp["Instances"][0]
        instid=inst["InstanceId"]
        print('Waiting for instance to enter running state')

        bIsRunning = False
        while bIsRunning == False:
            rz = cls.ec2.describe_instance_status(InstanceIds=[instid])
            #call can return before all data is available
            if not bool(rz):
                #sys.stdout.write('.')
                continue
            if len(rz["InstanceStatuses"]) == 0:
                #sys.stdout.write('.')
                continue

            inststate=rz["InstanceStatuses"][0]["InstanceState"]
            print(json.dumps(inststate,indent=2,separators=(',',':')))
            state=inststate["Name"]
            if state == 'running':
                bIsRunning = True
            #else:
                #sys.stdout.write('.')
                # 
            rz1 = cls.ec2.describe_instances(InstanceIds=[instid])
            if len(rz1["Reservations"]) == 0:
                continue

            instanceInfo = rz1["Reservations"][0]["Instances"][0]
            dns_name = instanceInfo['PublicDnsName']
            ip_address = instanceInfo['PublicIpAddress']

        print('EC2 instance is running')
        filename = 'instidfile' + instid
        os.system('rm -f %s ' % filename)
        bashcmd = 'echo ' + instid + ' > ' + filename
        os.system(bashcmd)

        return (inst, instid, dns_name, ip_address)

    @classmethod
    def create_volume(cls,inst,vpart,snapid = 0):

        instid=inst['InstanceId']
        #volume must be in same availability zone as instance
        azone=inst['Placement']['AvailabilityZone']
        #ec2=boto3.client('ec2',region_name=cls.region)
        if not snapid:
            resp = cls.ec2.create_volume(AvailabilityZone=azone, Size=2)
        else:
            resp=cls.ec2.create_volume(AvailabilityZone=azone,SnapshotId=snapid)

        volume_id = resp['VolumeId']
        #print('created volume in azone ' + azone + ' volumeId=' + volume_id +  ' snapid = ' + snapid)
        volume_state = resp.get('State')
        print('volume state=' + volume_state)

        #wait for the volume to be ready if needed
        bVolumeReady = False
        if (volume_state != 'creating'):
            bVolumeReady = True

        while not bVolumeReady:
            resp = cls.ec2.describe_volumes(VolumeIds=[volume_id])
            volume_state = resp['Volumes'][0]['State']
            print('volume state = ' + volume_state)
            if (volume_state == 'available'):
                bVolumeReady = True
            else:
                print('Volume is not ready')
                time.sleep(20)

        #attach volume to a device
        resp = cls.ec2.attach_volume(Device='/dev/' + vpart, InstanceId=instid,VolumeId=volume_id)
        print('attached volume to EC2 instance')
        filename = 'volumeidfile' + volume_id
        os.system('rm -f %s ' % filename)
        bashcmd = 'echo ' + volume_id + ' > ' + filename
        os.system(bashcmd)
        return volume_id

    @classmethod
    def create_snapshot(cls,volume_id):
        iz = random.randint(1, 9999999)
        snapshot_name = 'ucsc-aws-class-' + str(iz)
        resp = cls.ec2.create_snapshot(Description=snapshot_name, VolumeId=volume_id)
        print(resp)
        snapshot_id = resp.get('SnapshotId')
        # I incremented the number of tries up to 50 to assure that snapshot is complete
        numtries = 50  
        while numtries:
            response = cls.ec2.describe_snapshots(SnapshotIds=[snapshot_id,], )
            #print(response)
            if response['Snapshots'][0]['State'] == 'completed':
                break
            else:
                time.sleep(50)
                numtries = numtries - 1
                continue
        
        print('Created snapshot name=%s,id=%s' % (snapshot_name, snapshot_id))
        filename = 'snapshotid' + snapshot_id
        os.system('rm -f %s ' % filename)
        bashcmd = 'echo ' + snapshot_id + ' > ' + filename
        os.system(bashcmd)

        return snapshot_id

    @classmethod
    def terminate_instances(cls, instid):
        cls.ec2.terminate_instances(InstanceIds=[instid])
        print("terminated instance")

    @classmethod
    def connect_paramiko (cls, instance_id, dns_name,ip_address, commands1,commands2):
        print(instance_id+ ' paramiko ssh connect to ' + dns_name + ' ip:' + ip_address)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        tries = 1
        maxtries = 20
        sshloop = True
        while(sshloop):   
            try:          
                #ssh.connect(dns_name,username='ec2-user', key_filename=securitykey+'.pem')
                ssh.connect(ip_address,username='ec2-user', key_filename='.pem')
                sshloop = False
                print(str(ip_address) +  ' ssh connection successful')
            except paramiko.ssh_exception.NoValidConnectionsError as e:
                print(instance_id + "tries: " + str(tries) + " " + str(e.errors) +  ' ssh attempted')
                time.sleep(10)
                tries += 1
                if tries == maxtries:
                    raise

        print('running ' + commands1 + ' on ' + str(ip_address))
        stdin, stdout, stderr = ssh.exec_command(commands1)
        stdin.flush()
        data = stdout.read().splitlines()
        time.sleep(20)
        stdin, stdout, stderr = ssh.exec_command(commands2)
        stdin.flush()
        data1 = stdout.read().splitlines()
        time.sleep(60)
        ssh.close
        return data, data1

