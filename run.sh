#!/bin/bash

while getopts "d" flag
do
    case "${flag}" in
        d) dry=1;
    esac
done

set -e

if [ $dry ]; then
	python3 src/backend/app.py
	exit 
fi

docker stop site
docker container rm site
docker image rm economics_monitor

docker build -t economics_monitor .
docker run --name site -p 8080:8080 economics_monitor


