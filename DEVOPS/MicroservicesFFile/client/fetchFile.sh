#!/bin/bash

if [[ $# -ne 1 ]]; then
	echo "Please provide the filename that you want to fetch"
	exit
fi

fname=$1

curl -i 10.0.1.16:80/$fname


