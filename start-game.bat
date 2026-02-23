@echo off

:: Change to the directory where this script lives
:: (needed when double-clicking from Explorer)
cd /d "%~dp0"

echo Starting Word Learning Game...
echo.
echo The game will open in your browser at http://localhost:8000
echo.
echo To stop the server, close this window or press Ctrl+C
echo.

:: Start the browser after a short delay
start "" http://localhost:8000

:: Start Python server with SQLite history
python server.py
if errorlevel 1 (
    python3 server.py
)
if errorlevel 1 (
    echo.
    echo ERROR: Python is required to run this game.
    echo Please install Python from https://python.org
    echo.
    pause
)
