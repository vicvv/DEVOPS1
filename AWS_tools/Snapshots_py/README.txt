This is README file for Homeword 8.
The following files are inclued:
- AWS_8.py
- AWS_8_helper.py
- free_AWS_resources.py

While we can delete created instances, volumes and snapshots in our AWS_8 it 
is better to save instances, volumes and snpashots IDs in separate OS file and delete
them when we are ready by running free_AWS_resources.

AWS__helper has long sleep time for inststance to initialize. Apparantly if
instance in running but still initializing the snapshots of the volumes come out 
corrupted. So it is better wait untill instance is ready/ready 

Please read comments in all py files for details.

Usage:
All needed parametes are hardcoded in AWS_8_helper. In order to run the script please replace 
the hardcoded parameters with your own.
The script always works correctly in debug mode and not so correctly in run mode