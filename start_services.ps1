# PowerShell script to start Semantic Sales Analyzer services

Write-Host "=== Starting Semantic Sales Analyzer Services ===" -ForegroundColor Green

# Stop existing processes
Write-Host "`n1. Stopping existing services..." -ForegroundColor Yellow
try {
    Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
    Write-Host "[OK] Stopped existing Python processes" -ForegroundColor Green
} catch {
    Write-Host "[INFO] No existing processes found" -ForegroundColor Gray
}

# Start Backend
Write-Host "`n2. Starting Backend..." -ForegroundColor Yellow
try {
    Set-Location backend
    Start-Process -FilePath "python" -ArgumentList "main_simple.py" -NoNewWindow
    Write-Host "[OK] Backend starting on port 8000..." -ForegroundColor Green
    Start-Sleep -Seconds 3
} catch {
    Write-Host "[ERROR] Failed to start backend: $_" -ForegroundColor Red
    exit 1
}

# Start Frontend  
Write-Host "`n3. Starting Frontend..." -ForegroundColor Yellow
try {
    Set-Location ..\frontend
    Start-Process -FilePath "npm" -ArgumentList "start" -NoNewWindow
    Write-Host "[OK] Frontend starting on port 3000..." -ForegroundColor Green
    Write-Host "[INFO] Waiting for frontend to compile (30-60 seconds)..." -ForegroundColor Gray
} catch {
    Write-Host "[ERROR] Failed to start frontend: $_" -ForegroundColor Red
    exit 1
}

# Wait and check services
Write-Host "`n4. Checking services..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

$backendRunning = $false
$frontendRunning = $false
$dataLoaded = $false

# Check backend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/" -TimeoutSec 5 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        $backendRunning = $true
        Write-Host "[OK] Backend: RUNNING" -ForegroundColor Green
    }
} catch {
    Write-Host "[ERROR] Backend: NOT RUNNING" -ForegroundColor Red
}

# Check frontend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000/" -TimeoutSec 5 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        $frontendRunning = $true
        Write-Host "[OK] Frontend: RUNNING" -ForegroundColor Green
    }
} catch {
    Write-Host "[WARNING] Frontend may still be compiling..." -ForegroundColor Yellow
}

# Check data
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/data-summary" -TimeoutSec 5 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        $data = $response.Content | ConvertFrom-Json
        $dataLoaded = $true
        Write-Host "[OK] Data: LOADED ($($data.total_rows) rows)" -ForegroundColor Green
    }
} catch {
    Write-Host "[INFO] Data: Checking or not loaded" -ForegroundColor Gray
}

# Return to root
Set-Location ..

# Summary
Write-Host "`n" + ("=" * 50) -ForegroundColor Cyan
Write-Host "SERVICES STARTED!" -ForegroundColor Green
Write-Host ("=" * 50) -ForegroundColor Cyan

if ($backendRunning -and $frontendRunning) {
    Write-Host "SUCCESS: Both services are running!" -ForegroundColor Green
    Write-Host "`nAccess your application:" -ForegroundColor White
    Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
    Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
    
    if ($dataLoaded) {
        Write-Host "`nYour Sales Data.csv is ready for analysis!" -ForegroundColor Green
    } else {
        Write-Host "`nUpload Sales Data.csv when frontend is ready" -ForegroundColor Yellow
    }
    
    Write-Host "`nTo stop services:" -ForegroundColor Gray
    Write-Host "1. Close this terminal" -ForegroundColor White
    Write-Host "2. Or run: taskkill /F /IM python.exe" -ForegroundColor White
} else {
    Write-Host "ISSUE: Some services failed to start" -ForegroundColor Red
    Write-Host "Check the error messages above" -ForegroundColor Yellow
}

Write-Host ("=" * 50) -ForegroundColor Cyan
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
