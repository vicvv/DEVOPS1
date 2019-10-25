#!/bin/bash

RABBIT=$1

# Stop and remove existing docker entries
echo *** Stop webserver
docker stop daemon > /dev/null

echo *** Remove webserver image
docker rm daemon > /dev/null

# Build nameko service from Vagrant host
echo *** Build nameko service
cd /vagrant/daemon
docker build . -t daemon 

# Start docker daemon. The http server uses the nameko framework which runs on port 8000. Map this to port 80 on the Vagrant host
echo *** Run backend service 
docker run -d --name daemon -p 80:8000 daemon 

