#!/bin/bash

IMAGE_NAME="comfyui"
IMAGE_TAG="v1.0.1"
CONTAINER_NAME=$IMAGE_NAME

sudo docker stop $CONTAINER_NAME
sudo docker rm $CONTAINER_NAME
sudo docker rmi $IMAGE_NAME:$IMAGE_TAG
sudo docker build -t $IMAGE_NAME:$IMAGE_TAG .
sudo docker run -itd -p 11002:5000 -v /var/www/html/images/eo:/app/images/processed --name $CONTAINER_NAME $IMAGE_NAME:$IMAGE_TAG
