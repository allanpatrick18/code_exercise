#!/bin/sh
docker stop sports
echo "parou container"
docker rm sports
echo "removeu container"
docker build -t sports .
docker run -d --name=sports -p 9998:8080  sports