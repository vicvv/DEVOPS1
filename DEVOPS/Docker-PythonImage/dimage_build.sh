#!/bin/bash

echo " "
echo " This script does the following:

1.takes  command-line argument of the form repository:tag or exit the bash script with a usage message

2.creates a directory named n5, cd into n5
3.downloads - python/6/jessie Dockerfile using curl
4.Builds a docker image
5.Shows the new docker image is on your system
6.Tags the new Docker image using repository:tag – jessie:python3.6 
(the tag must be passed in as a command line argument to the script)
7.Shows that the Docker image is tagged
8. Runs the Docker image, non-interactively, verifying that Python 3.6 is installed "

echo " "

# procesing parameters
if [ $# = 1 ]; then
    echo "Your command line contains $# argument(s) which will be used as a tag: $1"
    mtag=$1
        
else
    echo "Some arguments are missing!"
    echo "Usage: $0 name:tag such as jessie:python3.6"
    exit 1   
fi

mkdir n5; cd n5;
curl https://raw.githubusercontent.com/docker-library/python/cf179e4a7b442b29d85f521c2b172b89ef04beef/3.6/jessie/Dockerfile -O
echo $mtag
docker build  -t ${mtag} .
echo " "
echo "Showing all docker images:"
docker images 
# why so many <none> ? To see use docker images -a?

echo " "
echo "The following python version is istalled:"; 
docker run --rm -ti ${mtag}  python --version;
echo " "


