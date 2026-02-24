@echo off

:: Change to the directory where this script lives
:: (needed when double-clicking from Explorer)
cd /d "%~dp0"

echo Starting Word Learning Game...
echo.

:: Check if Python is available BEFORE doing anything
python --version >nul 2>&1
if errorlevel 1 (
    python3 --version >nul 2>&1
    if errorlevel 1 (
        echo ============================================
        echo  ERROR: Python is not installed.
        echo ============================================
        echo.
        echo  Python is required to run this game.
        echo.
        echo  How to install Python on Windows:
        echo.
        echo  1. Go to https://www.python.org/downloads/
        echo  2. Click "Download Python 3.x.x"
        echo  3. Run the installer
        echo  4. IMPORTANT: Check the box
        echo     "Add Python to PATH"
        echo     at the bottom of the installer!
        echo  5. Click "Install Now"
        echo  6. Restart your computer
        echo  7. Double-click start-game.bat again
        echo.
        echo  Alternative: Install from Microsoft Store
        echo  - Open Microsoft Store
        echo  - Search for "Python 3"
        echo  - Click "Get" / "Install"
        echo.
        echo ============================================
        echo.
        pause
        exit /b 1
    )
)

echo The game will open in your browser at http://localhost:8000
echo.
echo To stop the server, close this window or press Ctrl+C
echo.

:: Start the browser after a short delay
start "" http://localhost:8000

:: Start Python server with SQLite history
python server.py 2>nul
if errorlevel 1 (
    python3 server.py
)
