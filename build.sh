#!/bin/bash

set -e

# Constants
SRC_DIR=src
DOCKER_DIR=Docker
DATA_DIR=data

# Copy the requirements.txt to Docker context if needed
# Build and run using docker-compose
docker compose down -v
echo "Building and starting containers..."
docker compose -f "compose.yaml" build
docker compose -f "compose.yaml" up
