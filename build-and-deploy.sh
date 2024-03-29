#!/bin/bash

# Exit script if any command fails
set -e

# Define variables
IMAGE_NAME="index-nft"
IMAGE_TAG="your_image_tag"
CONTAINER_NAME="index-nft-container"
PORT=8000

# Build the Docker image
echo "Building Docker image '$IMAGE_NAME:$IMAGE_TAG'..."
docker build -t $IMAGE_NAME:$IMAGE_TAG .

# Check if a container with the same name is already running, if so, stop it
if [ $(docker ps -q -f name=$CONTAINER_NAME) ]; then
    echo "A container with the name '$CONTAINER_NAME' is already running. Stopping it..."
    docker stop $CONTAINER_NAME
fi

# Remove the container if it exists
if [ $(docker ps -aq -f name=$CONTAINER_NAME) ]; then
    echo "A container with the name '$CONTAINER_NAME' exists. Removing it..."
    docker rm $CONTAINER_NAME
fi

# Run the container from the image
echo "Running container '$CONTAINER_NAME' from image '$IMAGE_NAME:$IMAGE_TAG'..."
docker run --name $CONTAINER_NAME --env-file .env -d -p $PORT:$PORT $IMAGE_NAME:$IMAGE_TAG

echo "Container '$CONTAINER_NAME' is running on port $PORT."
