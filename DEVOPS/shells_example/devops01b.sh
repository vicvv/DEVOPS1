#!/bin/bash

corecount=$(sysctl -a | grep machdep.cpu | grep core_count)
processor=$(sysctl -n machdep.cpu.brand_string)
mymem=$(system_profiler SPHardwareDataType | grep "  Memory:")
macaddr=$(ifconfig -a | grep ether| head -1)

# procesing parameters
if [ $# = 1 ]; then
    myparam=$1
    echo -n "Checking "
    echo $myparam

else    
    echo "Incorect usage. Must be $0 and one of the parameters such as all, volume, cpu, network, ram"
    echo "Check the usage and try again!"
    exit 1   
fi

if [ $myparam == 'all' ]; then
    #df -Ph | awk 'NR == 1 || $0 ~ "^/dev/"'
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

elif [ $myparam == 'volumes' ]; then
    df -Ph | awk 'NR == 1 || $0 ~ "^/dev/"'
elif [ $myparam == 'cpu' ]; then
    echo -n "Number CPU/Cores: "
    echo $corecount
elif [ $myparam == 'network' ]; then
    echo -n "MACADDRESS: "
    echo $macaddr
    echo -n "My Public IP:"
    curl ifconfig.me
    echo " "
elif [ $myparam == 'ram' ]; then 
    echo -n "RAM "
    echo $mymem
fi


