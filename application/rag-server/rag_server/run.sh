#!/bin/bash
# This script is intended to be run with rag-server/rag_server as the cwd

docker pull qdrant/qdrant:v1.10.1
docker run -d -p 6333:6333 qdrant/qdrant:v1.10.1

# Allow qdrant to initialize
echo "Giving qdrant container some time to initialize"

# TODO: we could poll for the container status but this should work 
sleep 3

# Restores snapshot of db from remote
echo "Sending request to restore snapshot"
poetry run python ./initialize_qdrant.py

# Initializes server
echo "Initializing workers"
poetry run uvicorn main:app --workers 9 --host 0.0.0.0 --port 8000