#!/bin/bash

BACKEND_IP=$1

# Stop and remove existing docker entries

echo *** Stopping frontend process
docker stop frontend > /dev/null

echo *** Removig frontend process
docker rm frontend > /dev/null

# Build ws client from inside Vagrant host
echo *** Build frontend client
cd /vagrant/web
docker build . -t u:frontend

# Start docker ws service in background as frontend
echo *** Run frontend client and map to port 8000 on Vagrant host
docker run -d --name frontend -p 80:8000 -e BACKEND_IP=${BACKEND_IP} u:frontend

