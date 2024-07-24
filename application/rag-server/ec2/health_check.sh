#!/bin/bash

# Health check URL
HEALTH_CHECK_URL="http://localhost:8000/v1/health"

# Function to check the health
check_health() {
    STATUS_CODE=$(curl -o /dev/null -s -w "%{http_code}\n" $HEALTH_CHECK_URL)
    if [ "$STATUS_CODE" -ne 200 ]; then
        echo "$(date): Health check failed with status code $STATUS_CODE. Restarting FastAPI service."
        sudo systemctl restart rag-api.service
    else
        echo "$(date): Health check passed with status code $STATUS_CODE."
    fi
}

# Run the health check
check_health
