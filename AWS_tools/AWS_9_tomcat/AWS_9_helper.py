# -*- coding: utf-8 -*-

import os, sys, time, timeit, inspect, subprocess
import boto3
import botocore
import subprocess
import paramiko
import urllib.request
import urllib.error
from scp import SCPClient
from botocore.exceptions import ClientError

class Insclass:
    # class variable collects instanse id and region to be further used for clenup/delete
    instanceIds = [ ]
    regions = [ ]
    # class constant
    instance_type = 't2.micro'
    
    def __init__(self, ami_instance=None, securitygroup=None,securitykey=None,region=None, numofinstances = None):
        self.ami_instance = ami_instance
        self.secgrp = securitygroup
        self.securitykey = securitykey
        self.region = region
        self.nuinst = numofinstances

    # this method gets security group id with give group name    
    def findsecgrid(self, secgrp, region):
        ec2 = boto3.client('ec2',region_name=region)
        try:
            response = ec2.describe_security_groups(
                Filters=[
                    dict(Name='group-name', Values=[secgrp])
                ]
            )
            return response['SecurityGroups'][0]['GroupId']

        except ClientError as e:
            print(e)
            return None

    # this methods is used to check instantce startup status. Very important!
    def waitForStatus(self,status, client, instance, delay, max_attempts):
        try:
           waiter = client.get_waiter(status)
        except ValueError as e:
            print(inspect.stack()[0][3] + " wait status error:" + str(e))  
            print("terminating program")
            return None
               
        print("Default waiter delay in seconds: " + str(waiter.config.delay) )
        print("Default waiter max attempts: " + str(waiter.config.max_attempts)) 
        print("Default maximum waiter wait time in minutes: "+ str((waiter.config.delay+waiter.config.max_attempts)/60))
        waiter.config.delay = delay
        waiter.config.max_attempts = max_attempts
        print( "Reset waiter delay in seconds: " + str(waiter.config.delay) )
        print( "Reset waiter max attempts: " + str(waiter.config.max_attempts) ) 
        print("Each wait is <= " + str(delay*max_attempts) + " seconds" )        
        
        maxLoops = 12
        start_time = timeit.default_timer()   
        print("loop <= " + str(maxLoops) + " times, each time issuing a wait for " + status + ", with a maximum wait time of " + str(delay * max_attempts) + " seconds")
        instid = instance['InstanceId']
        for loop in range (1, maxLoops): 
            print ("loop # " + str(loop) + " for instance " + instid + "," + status)
            try:   
                    waiter.wait(InstanceIds=[instid])
                    print("wait success for: "+ str(instid))
                    elapsed = timeit.default_timer() - start_time
                    print("time for wait: " + str(elapsed/60)+ " minutes")
                    return "Ok"  # we can break from loop with return
            except botocore.exceptions.WaiterError as e:
                    print("wait error " + str( e ))
                    waiter = client.get_waiter(status)  # must reset the waiter for each wait
                    waiter.config.delay = delay
                    waiter.config.max_attempts = max_attempts
                    elapsed = timeit.default_timer() - start_time
                    print("time for wait: " + str(elapsed/60)+ " minutes")
                    pass
        

    # this method starts the instance
    def startinstance(self,secgrp,ami_instance,securitykey,region,count):
        ec2 = boto3.client('ec2',region_name=region)
        securitygroupid = self.findsecgrid(secgrp,region)
        resp = ec2.describe_vpcs()
        vpcidtouse = resp['Vpcs'][0]['VpcId']
        subnetlist = ec2.describe_subnets(Filters=[{'Name':'vpc-id', 'Values':[vpcidtouse]}])
        subnetid = subnetlist['Subnets'][0]['SubnetId']
        secgrpidlist=[str(securitygroupid)]
        #secgrpidlist=[securitygroupid[1:-1]]
        resp = ec2.run_instances(ImageId=ami_instance,InstanceType=Insclass.instance_type,
                                KeyName=securitykey,SecurityGroupIds = secgrpidlist,
                                SubnetId=subnetid, MinCount=1, MaxCount=count)

        instList = resp["Instances"]
         
        loopCnt = 0   
        for instance in instList:
            instid = instance['InstanceId']
            Insclass.instanceIds.append(instid)  #save the instance Ids for deletion
            Insclass.regions.append(region)

            print(str(loopCnt))
            print ("Invoking wait for instance " + instid)
            result = self.waitForStatus('instance_running', ec2, instance, 25, 2)
            if not result:
                print("Check waitForStatus function")

            print('The following instance has been started: ' + instid + 'in region ' + region +   ' waiting for public DNS name')
            haveDNS = False
            maxDNSTries = 16
            sleepTime = 2
            while haveDNS == False and maxDNSTries > 0:
                time.sleep(sleepTime)
                rz=ec2.describe_instance_status(InstanceIds=[instid])
                if not bool(rz):
                    continue
                if len(rz["InstanceStatuses"]) == 0:
                    continue
                inststate = rz["InstanceStatuses"][0]["InstanceState"]
                state=inststate["Name"]
                if state != 'running':
                    continue               
                rz1 = ec2.describe_instances(InstanceIds=[instid])
                if len(rz1["Reservations"]) == 0:
                    continue
                instanceInfo = rz1["Reservations"][0]["Instances"][0]
                dns_name = instanceInfo['PublicDnsName']
                ip_address = instanceInfo['PublicIpAddress']
                maxDNSTries -= 1
                if dns_name and ip_address:
                    break
            
            if not dns_name:
                print('cannot get DNS Name for instance:' + instid)
                return
            
        return instid, dns_name, ip_address

    # this method starts ssh connection
    def connectssh(self,instid,ip_address,securitykey):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        tries = 1
        maxtries = 5
        sshloop = True
        while(sshloop):  
            try:           
                ssh.connect(ip_address,username='ec2-user', key_filename=securitykey+'.pem')
                sshloop = False
                print(str(ip_address) +  ' ssh connection successful')
                return ssh
            except paramiko.ssh_exception.NoValidConnectionsError as e:
                print(instid + "tries: " + str(tries) + " " + str(e.errors) +  ' ssh attempted')
                time.sleep(10)
                tries += 1
                if tries == maxtries:
                    raise

    # this method to test url connection
    def testconnection(self,ip_address, instid, prt):
        tries = 1
        maxtries = 5
        urlloop = True
        while(urlloop):
            try:       
                urloutput = urllib.request.urlopen("http://"+ ip_address + prt).read()
                urlloop = False
            except:
                print(str(instid) + " " + str(tries)  + ' urlopen attempted')
                time.sleep(10)
                tries += 1
                if tries == maxtries:
                    print('ERROR: hit maxtries:' + str(maxtries) + ' urlopen ' + "http://" +ip_address + prt)
                    raise
                        
        if 'Congratulations!'  or 'Clock' in urloutput.decode():
            print( str(ip_address) +  " successful connection to Tomcat")
            print("Successful connection to http://" + str(ip_address) + prt)

        else:
            print("Connection to Tomcat failed, for instance " + str(ip_address)) 
            print(urloutput)
        
    # this method installs and starts tomcat  server 
    def start_tomcat(self,instid, dns_name, ip_address, securitykey, region) :
        print(instid + ' paramiko ssh connect to ' + dns_name + ' ip:' + ip_address)

        # code to start tomcat starts here
        ssh = self.connectssh(instid,ip_address,securitykey)

        # this is a AWS Linux server, install pending updates
        print('updating yum on ' + str(ip_address))

        stdin, stdout, stderr = ssh.exec_command("sudo yum -y update")
        stdin.flush()
        
        print('installing tomcat on ' + str(ip_address))
        stdin, stdout, stderr = ssh.exec_command("sudo yum -y install tomcat8 tomcat8-webapps")
        stdin.flush()
        data = stdout.read().splitlines()
        if data[-1].decode() == 'Complete!':
            print(ip_address + ' tomcat install successful on ' + str(ip_address))
        else:
            print(str(ip_address) + ' tomcat did NOT install')
            return
        print('starting tomcat on ' + str(ip_address))
        stdin, stdout, stderr = ssh.exec_command("sudo service tomcat8 start")
        stdin.flush()
        data = stdout.read().splitlines()
        #data is binary so convert to a string
        if 'OK' in data[-1].decode():
            print('tomcat start successful on ' + str(ip_address))
        else:
            print('could NOT start tomcat on ' + str(ip_address))
            return

        print('getting tomcat status from ' + str(ip_address))
        stdin, stdout, stderr = ssh.exec_command("sudo service tomcat8 status")
        stdin.flush()
        data = stdout.read().splitlines()
        if 'running' in data[-1].decode():
            print('confirmed tomcat service is running on' + str(ip_address))
        else:
            print('could not determine if tomcat is running on ' + str(ip_address))

        print("testing Tomcat, connecting to http://" + str(ip_address) + ":8080")

        self.testconnection(ip_address, instid, ':8080')
        
        # end of loop for processing created instances
        print('closing ssh connection to ', str(ip_address))
        ssh.close

    # this methods move my web app and installs it in tomcat
    def movemyapp(self,instid,ip_address,securitykey):
        ssh = self.connectssh(instid,ip_address,securitykey)
        
        stdin, stdout, stderr = ssh.exec_command("sudo mkdir /var/lib/tomcat8/webapps/MyApp")
        stdin.flush()
        
        stdin, stdout, stderr = ssh.exec_command("sudo chmod 777 /var/lib/tomcat8/webapps/MyApp")
        stdin.flush()
        
        # preparing MyApp files for scp
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        print (fileDir)
        cwd = os.getcwd()
        print(cwd)

        #For accessing the file in a folder contained in the current folder
        filename = os.path.join(cwd, 'MyApp/index.html')
        print(filename)
        with open(filename, 'w') as fn:
            try: 
                fn.write('<meta http-equiv="Refresh" content="1; url=http://' + str(ip_address) + ':8080/MyApp/MyWebApp.html">')
                # fn.write("hi")
            except IOError as e:
                print(e,'error')
        with open(filename, 'r') as fin:
                print(fin.read())

        print("http://" + str(ip_address) + ":8080/MyApp/MyWebApp.html")
        
        # SCPCLient takes a paramiko transport as an argument
        scp = SCPClient(ssh.get_transport())
        scp.put('MyApp', recursive=True, remote_path='/var/lib/tomcat8/webapps/')

        self.testconnection(ip_address, instid, ':8080/MyApp/MyWebApp.html')

        stdin, stdout, stderr = ssh.exec_command("sudo chown -R tomcat:tomcat /var/lib/tomcat8/webapps/MyApp")
        stdin.flush()

        stdin, stdout, stderr = ssh.exec_command("sudo chmod 755 /var/lib/tomcat8/webapps/MyApp")
        stdin.flush()

        stdin, stdout, stderr = ssh.exec_command("sudo chmod 644 /var/lib/tomcat8/webapps/MyApp/*")
        stdin.flush()

        print('closing ssh connection to ', str(ip_address))
        ssh.close

    # this method is used only if we want to delete instance after they were created. 
    # otherwise please use delete_instances.py file to clean up (included)
    @classmethod
    def delete_instance(clm,instanceIds, region):  
        print(type(instanceIds), instanceIds) 
        ec2 = boto3.client('ec2',region_name=region) 
        response=ec2.terminate_instances(InstanceIds=(instanceIds,)) #JSON is returned
        print ('The following instances have been queued for termination: ', instanceIds, response) 

 