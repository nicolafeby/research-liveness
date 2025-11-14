#!/bin/bash

echo "Building Docker image..."
docker build -t liveness-poc .

echo "Stopping and removing old container (if exists)..."
docker stop liveness 2>/dev/null
docker rm liveness 2>/dev/null

echo "Running container..."
docker run -d --name liveness -p 8000:8000 liveness-poc

echo "Done! Container is running at http://localhost:8000"
