#!/bin/bash

# This will build the backend and frontend vagrant hosts


# Define environment variables for frontend and backend IP
# These are references in the following files:
# backend\Vagrantfile
# frontend\Vagrantfile
# frontend\deploy_docker_frontend.bash
# frontend\web\ip.yaml

export FRONTEND_IP=10.0.1.16
export BACKEND_IP=10.0.1.17


# Build backend service 
cd backend

vagrant up

cd ..

# Build frontend webservice. 

cd frontend

vagrant up



# Valid queries to frontend
# *** The trailing url slash is required as shown to avoid an unresolved 301 redirect.
# http://<frontend ip>:80/
# http://<frontend ip>:80/grab/cpu_times/
# http://<frontend ip>:80/grab/swap_memory/
# http://<frontend ip>:80/grab/virtual_memory/
# http://<frontend ip>:80/grab/net_if_addrs/


cd ..


# Misc Notes

# To recompile web server on frontend from /frontend outside vagrant
# vagrant provision --provision-with frontend

# To recompile web server on backend from /backend outside vagrant
# vagrant provision --provision-with backend

# To see logs on frontend from /frontend outside vagrant
# vagrant ssh -- 'docker logs ws'

# To see logs on backend from /backend outside vagrant
# vagrant ssh -- 'docker logs daemon'

# To test frontend from /frontend outside vagrant
# vagrant ssh -- 'curl localhost'

# To test backend from /backend outside vagrant
# vagrant ssh -- 'curl localhost'
