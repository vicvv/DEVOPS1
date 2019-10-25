#!/bin/bash

RABBIT=$1

# Stop and remove existing docker entries
echo *** Stop webserver
docker stop backend > /dev/null

echo *** Remove webserver image
docker rm backend > /dev/null

# Build nameko service from Vagrant host
echo *** Build nameko service
cd /vagrant/backend
docker build . -t u:backend 

# Start docker daemon. The http server uses the nameko framework which runs on port 8000. Map this to port 80 on the Vagrant host
echo *** Run backend service 
docker run -d --name backend -p 80:8000 u:backend

