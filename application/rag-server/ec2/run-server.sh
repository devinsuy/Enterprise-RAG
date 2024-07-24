#!/bin/bash
source activate pytorch
cd /home/ec2-user/Enterprise-RAG/application/rag-server/rag_server

# Run the new run.sh script in headless mode with custom log file
nohup ./run.sh > /home/ec2-user/Enterprise-RAG/application/rag-server/server.log 2>&1 &

# Get logs with: tail -f nohup.out
# Find process with: ps -ef | grep python
# Kill process with: kill <PID>
# Sleep to keep the script running
sleep infinity
