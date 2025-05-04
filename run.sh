#!/bin/bash


docker stop site
docker container rm site
docker image rm economics_monitor

docker build -t economics_monitor .
docker run --name site -p 8080:8080 economics_monitor


