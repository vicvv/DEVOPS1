import boto3
import json

region='us-west-1'
#http://boto3.readthedocs.io/en/latest/reference/core/boto3.html
ec2c=boto3.client('ec2',region_name=region)

#get the 1st vpc and 1st subnet
resp=ec2c.describe_vpcs()
vpcidtouse=resp['Vpcs'][0]['VpcId']
subnetlist=ec2c.describe_subnets(Filters=[ {'Name': 'vpc-id', 'Values': [vpcidtouse]} ])
subnetid = subnetlist['Subnets'][0]['SubnetId']

#uncomment this to see format of response from describe_subnets
#print(json.dumps(subnetlist,indent=2,separators=(',',':')))

secgrpname='awsclass01'

try:	
	secgrpfilter = [
		{
			'Name':'group-name', 'Values':[secgrpname]
		}
	]
	secgroups = ec2c.describe_security_groups(
		Filters=secgrpfilter
	)
	secgrptouse = secgroups["SecurityGroups"][0]
	secgrpid = secgrptouse['GroupId']
except:
	secgrptouse = ec2c.create_security_group(
		GroupName=secgrpname,Description='aws class open ssh,http,https',
		VpcId=vpcidtouse)
	secgrpid = secgrptouse['GroupId']
	print("created security group:" + secgrpid)

	#open ports 22, 80, 443, 
	portlist = [22, 80, 443]
	for port in portlist:
		try:
			ec2c.authorize_security_group_ingress(
				CidrIp='0.0.0.0/0',
				FromPort=port,
				GroupId=secgrpid,
				IpProtocol='tcp',
				ToPort=port)
		except:
			print("error opening port:" +  str(port))
			exit()
		

if secgrptouse is None or secgrptouse is NameError:
	print('cannot continue no security group')
	exit()

#start instance
#amiid='ami-824c4ee2'
amiid='ami-0ec6517f6edbf8044'
insttype='t2.micro'
secgrpidlist=[secgrpid]
sshkeypair = 'vitoshkav64'
numinstances = 1

resp = ec2c.run_instances(
    ImageId=amiid, 
    InstanceType=insttype,
    KeyName=sshkeypair,
    SecurityGroupIds=secgrpidlist,
	SubnetId=subnetid,
    MaxCount=numinstances,
    MinCount=numinstances)

#wait until instance is running
inst=resp["Instances"][0]
instid=inst["InstanceId"]
print('Waiting for instance to enter running state')

bIsRunning = False
while bIsRunning == False:
	rz=ec2c.describe_instance_status(InstanceIds=[instid])
	#call can return before all data is available
	if not bool(rz):
		print('.')
		continue
	if len(rz["InstanceStatuses"]) == 0:
		print('.')
		continue
	#rz["InstanceStatuses"][0]["InstanceState"]["Name"]
	#print(json.dumps(rz,indent=2,separators=(',',':')))

	inststate=rz["InstanceStatuses"][0]["InstanceState"]
	print(json.dumps(inststate,indent=2,separators=(',',':')))
	state=inststate["Name"]
	if state == 'running':
		bIsRunning = True
	else:
		print('.')

print(' ')

#get ip
bGotIp = False
while bGotIp == False:
	outp = ec2c.describe_instances(InstanceIds=[instid])
	inst=outp["Reservations"][0]["Instances"][0]
	instid=inst["InstanceId"]
	#publicip=inst["PublicIpAddress"]
	publicip=inst.get('PublicIpAddress')
	if not publicip:
		print('do not have ip address yet')
		continue
	else:
		bGotIp = True

print('ip=' + publicip)

#terminate
input('press enter to stop and terminate instance')
resp=ec2c.stop_instances(InstanceIds=[instid])
print(json.dumps(resp,indent=2,separators=(',',':')))

resp=ec2c.terminate_instances(InstanceIds=[instid])
print(json.dumps(resp,indent=2,separators=(',',':')))

	

