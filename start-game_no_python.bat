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

:: Start PowerShell HTTP server (no Python required)
powershell -ExecutionPolicy Bypass -Command "$listener = New-Object System.Net.HttpListener; $listener.Prefixes.Add('http://localhost:8000/'); $listener.Start(); Write-Host 'Server running at http://localhost:8000/ - Press Ctrl+C to stop'; while ($listener.IsListening) { $context = $listener.GetContext(); $request = $context.Request; $response = $context.Response; $localPath = $request.Url.LocalPath; if ($localPath -eq '/') { $localPath = '/index.html' }; $filePath = Join-Path (Get-Location) $localPath.TrimStart('/'); if (Test-Path $filePath -PathType Leaf) { $content = [System.IO.File]::ReadAllBytes($filePath); $ext = [System.IO.Path]::GetExtension($filePath).ToLower(); $contentType = switch ($ext) { '.html' {'text/html'} '.css' {'text/css'} '.js' {'application/javascript'} '.json' {'application/json'} '.png' {'image/png'} '.jpg' {'image/jpeg'} '.gif' {'image/gif'} '.svg' {'image/svg+xml'} '.ico' {'image/x-icon'} default {'application/octet-stream'} }; $response.ContentType = $contentType; $response.ContentLength64 = $content.Length; $response.OutputStream.Write($content, 0, $content.Length) } else { $response.StatusCode = 404; $errorMsg = [System.Text.Encoding]::UTF8.GetBytes('404 - File Not Found'); $response.OutputStream.Write($errorMsg, 0, $errorMsg.Length) }; $response.Close(); Write-Host \"$($request.HttpMethod) $($request.Url.LocalPath)\" }"

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start the PowerShell HTTP server.
    echo.
    echo Please make sure PowerShell is available on your system.
    echo.
    pause
)
