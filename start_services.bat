@echo off
echo === Starting Semantic Sales Analyzer Services ===
echo.

echo 1. Stopping existing services...
taskkill /F /IM python.exe >nul 2>&1
echo [OK] Stopped existing processes

echo.
echo 2. Starting Backend...
cd /d "%~dp0backend"
start /B python main_simple.py
echo [OK] Backend starting on port 8000...

echo.
echo 3. Starting Frontend...
cd /d "%~dp0frontend"
start /B npm start
echo [OK] Frontend starting on port 3000...

echo.
echo 4. Waiting for services to start...
timeout /t 10 /nobreak >nul

echo.
echo === Services Starting ===
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo.
echo Your Sales Data.csv will be ready for analysis!
echo.
echo Close this window to keep services running in background
echo Or press Ctrl+C to stop

pause
