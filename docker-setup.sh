#!/bin/sh -x

# create docker image
docker build -f .devcontainer/Dockerfile -t pldi:v1 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .

# start docker image
docker run --name pldi -dit --mount type=bind,source="$(pwd)",target=/home/vscode/PLDI-Mini-Conf --workdir /home/vscode/PLDI-Mini-Conf --user "$(id -u):$(id -g)" --expose 5000 -p 5000:5000 pldi:v1

