#!/bin/bash
# --- Part 02

# a) in folder DevOps01, create a bash script called devops01a.sh that 
#   gets information about your computer including:
#   number of volumes, size of each volume, free space on each volume
#   number cpus/cores, information about the cpus/core, amount of ram, 
#   your mac address and ip address
#   print these details out

# NOTE: there are a number of ways to get this information from Bash, you can do web searches to get info on this
# b) periodically, stage this file and commit it locally in git
# c) periodically commit this file to the remote GitHub repo

#system_profiler SPHardwareDataType | grep "  Memory:"
#system_profiler SPHardwareDataType | grep Cores:
#system_profiler SPHardwareDataType | grep Processors:

mkdir tmp
echo "Information about my computer"
#echo $volumesinfo
df -Ph | awk 'NR == 1 || $0 ~ "^/dev/"'
numofvolumes=$(df -Ph | awk 'NR == 1 || $0 ~ "^/dev/"' | grep dev | wc -l)
corecount=$(sysctl -a | grep machdep.cpu | grep core_count)
processor=$(sysctl -n machdep.cpu.brand_string)
mymem=$(system_profiler SPHardwareDataType | grep "  Memory:")
macaddr=$(ifconfig -a | grep ether| head -1)

echo " "
echo -n "Number of Volumes: "
echo $numofvolumes

echo " "
i=1
df -Ph | awk 'NR == 1 || $0 ~ "^/dev/"'| grep dev > tmp/du$$

while read line
do
    echo -n "Device #${i} "
    echo $line | awk '{print $1}'
    echo -n "Total Size on Device #${i}: "
    echo $line | awk '{print $2}'
    echo -n "Free space on Device #${i}: "
    echo $line | awk '{print $4}'
    ((i+=1))
done < tmp/du$$
rm tmp/du$$

echo " "
echo -n "Number CPU/Cores: "
echo $corecount
echo -n "My MAC processor: "
echo $processor
echo -n "RAM "
echo $mymem
echo -n "MACADDRESS: "
echo $macaddr

echo -n "My Public IP:"
curl ifconfig.me
echo " "

# macstaff=$(diskutil list)
# echo -n "Output from discutil list on my MAC: "
# echo $macstaff