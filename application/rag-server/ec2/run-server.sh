#!/bin/bash
source activate pytorch

# This path assumes you are at home directory ~
cd ./Enterprise-RAG/application/rag-server

# Run server in headless mode
# Get logs with: tail -f nohup.out
# Find process with: ps -ef | grep python
# Kill process with: kill <PID>
nohup poetry run python rag_server/main.py &
