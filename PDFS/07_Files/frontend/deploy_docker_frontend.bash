#!/bin/bash

BACKEND_IP=$1

# Stop and remove existing docker entries

echo *** Stopping ws process
docker stop ws > /dev/null

echo *** Removig ws process
docker rm ws > /dev/null

# Build ws client from inside Vagrant host
echo *** Build ws client
cd /vagrant/web
docker build . -t ws

# Start docker ws service in background as ws
echo *** Run ws client and map to port 80 on Vagrant host
docker run -d --name ws -p 80:8000 -e BACKEND_IP=${BACKEND_IP} ws

