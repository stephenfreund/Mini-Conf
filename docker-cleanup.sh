#!/bin/sh -x

# stop and delete any docker instances named 'pldi'
docker stop pldi
docker rm pldi
docker rmi pldi:v1
