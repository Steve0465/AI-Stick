#!/bin/bash
# Stop AI Stick services

cd "$(dirname "$0")/docker"
echo "🛑 Stopping AI Stick..."
docker compose down
echo "✅ All services stopped."
