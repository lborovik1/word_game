#!/bin/bash

# Change to the directory where this script lives
# (needed when double-clicking from Finder)
cd "$(dirname "$0")"

echo "Starting Word Learning Game..."
echo ""
echo "The game will open in your browser at http://localhost:8000"
echo ""
echo "To stop the server, press Ctrl+C"
echo ""

# Open browser (works on Mac and Linux)
if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost:8000
else
    xdg-open http://localhost:8000 2>/dev/null || sensible-browser http://localhost:8000 2>/dev/null &
fi

# Start Python server with SQLite history
python3 server.py 2>/dev/null || python server.py
