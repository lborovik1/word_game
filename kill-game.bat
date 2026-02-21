@echo off

:: Change to the directory where this script lives
:: (needed when double-clicking from Explorer)
cd /d "%~dp0"

echo Stopping Word Learning Game server...
echo.

:: Find and kill processes on port 8000
set FOUND=0

for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000 " ^| findstr "LISTENING"') do (
    echo Found server process: %%a
    taskkill /PID %%a /F >nul 2>&1
    set FOUND=1
)

if %FOUND%==0 (
    echo No server found running on port 8000.
) else (
    echo Server stopped successfully.
)

echo.
echo Done.
echo.
pause
