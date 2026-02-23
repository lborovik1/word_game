#!/bin/bash

# Change to the directory where this script lives
# (needed when double-clicking from Finder)
cd "$(dirname "$0")"

echo "Stopping Word Learning Game server..."
echo ""

# Find and kill server.py or python http server on port 8000
PIDS=$(lsof -ti:8000 2>/dev/null)

if [ -z "$PIDS" ]; then
    echo "No server found running on port 8000."
else
    echo "Found server process(es): $PIDS"
    echo "$PIDS" | xargs kill 2>/dev/null
    sleep 1
    # Force kill if still running
    REMAINING=$(lsof -ti:8000 2>/dev/null)
    if [ -n "$REMAINING" ]; then
        echo "$REMAINING" | xargs kill -9 2>/dev/null
        echo "Force-killed remaining processes."
    fi
    echo "Server stopped successfully."
fi

echo ""
echo "Done. You can close this window."

# Keep window open briefly when double-clicked
sleep 2
