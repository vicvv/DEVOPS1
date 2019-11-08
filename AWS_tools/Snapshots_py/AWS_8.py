import os
import time
import sys
import boto3
import botocore
import botocore.exceptions
from botocore.exceptions import ClientError
import json
import random
from AWS_8_helper import Createinstance
import glob
import time
import paramiko

# instantiating the class
myinst = Createinstance()

ssh = paramiko.SSHClient()
cwd = os.getcwd()

# creating an instance
print("Starting the first instance ....")
(instance, instance_id, dns_name, ip_address) = myinst.launch_instance()

# creating and attaching volume sto the instance
print("Creating and attaching first volume ...")
volume_id = myinst.create_volume(instance,'sdf')
print(volume_id)
print("Creating and attaching second volume ...")
volume_id2 = myinst.create_volume(instance, 'sdp')
print(volume_id2)

# preparing commands for piramiko and running piramiko
print("Connecting ssh ...")
commands1 = '''sudo file -s /dev/sdf;sudo file -s /dev/xvdf;sudo mke2fs -t ext4 -F -j /dev/sdf;sudo mkdir /mnt/cats_data;sudo mount /dev/sdf /mnt/cats_data;cd /mnt/cats_data;sudo chmod 777 .;echo "Hello cats" > cats_file.txt; sudo file -s /dev/xvdf;'''
commands2 = '''sudo file -s /dev/sdp;sudo file -s /dev/xvdp;sudo mke2fs -t ext4 -F -j /dev/sdp;sudo mkdir /mnt/dogs_data;sudo mount /dev/sdp /mnt/dogs_data;cd /mnt/dogs_data;sudo chmod 777 .;echo "Hello dogs" > dogs_file.txt; sudo file -s /dev/xvdp;'''
(data, data1) = myinst.connect_paramiko(instance_id,dns_name, ip_address, commands1, commands2)
print(data, data1)

# taking shapshots of previously created volumes
print("Taking first snapshot ...")
snapshot_id = myinst.create_snapshot(volume_id)
print(snapshot_id)
time.sleep(60)
print("Taking second snapshot ...")
snapshot_id2 = myinst.create_snapshot(volume_id2)
print(snapshot_id)
time.sleep(60)


# while creating snpashots I recorede snapshotids in separate file.
# now I am accessing the file and aquiering my snapshots ids
snapshotfile = 'snapshotid*'
# reserving the letters for future devices
myarr = ['f','p']
# creating new instance
print("Creating a new instance ....")
(instance_new, instance_id,dns_name, ip_address) = myinst.launch_instance()
time.sleep(60)
# accessing OS files with the snapshot information and creating volumes using 
# accuired snapshot ids
index = 0
for filename in glob.glob(os.path.join(cwd, snapshotfile)):
    if os.path.exists(filename) == False:
        print(filename + " does not exist")
        quit()
    else:       
        fileobj = open(filename, 'r')
        snapidP = fileobj.read()
        snapid = snapidP.strip().strip('\n\r')
        fileobj.close()
        print("using snapshot-id:" + snapid + " to create a new volume")      
        volume_id = myinst.create_volume(instance_new,'sd'+ myarr[index], snapid)
        time.sleep(60)
        print(volume_id)   
        index = index + 1

# preparing commands for piramico restore action
commands1r = '''sudo file -s /dev/xvdf;sudo mkdir /mnt/restore_1;sudo mount /dev/sdf /mnt/restore_1 -t ext4;cd /mnt/restore_1;cat *file.txt;'''
commands2r = '''sudo file -s /dev/xvdp;sudo mkdir /mnt/restore_2;sudo mount /dev/sdp /mnt/restore_2 -t ext4;cd /mnt/restore_2;cat *file.txt;'''

# calling piramico and mounting volumes created from snapshots to new instance
print("Connecting to the instance with ssh .....")
(data, data1) = myinst.connect_paramiko(instance_id, dns_name, ip_address, commands1r, commands2r)
print(data, data1)

# below are comments for my personal use
# before snapshot
'''
cat /proc/partitions;
lsblk;
sudo file -s /dev/sdf;
sudo file -s /dev/xvdf;
ls /dev/sdf;

sudo mke2fs -t ext4 -F -j /dev/sdf;
sudo mkdir /mnt/cats_data;
sudo mount /dev/sdf /mnt/cats_data;
df -T;
cd /mnt/cats_data;
sudo chmod 777 .;
echo "Hello cats" > cats_file.txt;
cat cats_file.txt;
sudo file -s /dev/xvdf;


cat /proc/partitions;
lsblk;
sudo file -s /dev/sdp;
sudo file -s /dev/xvdp;
ls /dev/sdp;

sudo mke2fs -t ext4 -F -j /dev/sdp;
sudo mkdir /mnt/dogs_data;
sudo mount /dev/sdp /mnt/dogs_data;
df -T;
cd /mnt/dogs_data;
sudo chmod 777 .;
echo "Hello dogs" > dogs_file.txt;
cat dogs_file.txt;
sudo file -s /dev/xvdp;

'''

#after shanpshots

'''
lsblk;
sudo file -s /dev/xvdf;
sudo mkdir /mnt/restore_cats;
sudo mount /dev/sdf /mnt/restore_cats -t ext4;
cd /mnt/restore_cats;
ls;
cat cats_file.txt;

lsblk;
sudo file -s /dev/xvdp;
sudo mkdir /mnt/restore_dogs;
sudo mount /dev/sdp /mnt/restore_dogs -t ext4;
cd /mnt/restore_dogs;
ls;
cat dogs_file.txt;

'''

