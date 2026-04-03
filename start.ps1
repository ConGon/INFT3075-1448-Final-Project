# ---------- CONFIG ----------
$backendPath = "server"
$frontendPath = "client"
$venvPath = "$backendPath\venv"
$ollamaPort = 11434
$modelName = "deepseek-r1:8b"

# ---------- FUNCTION TO ENSURE PORT IS FREE ----------
function Free-Port {
    param($Port)
    do {
        $connections = netstat -aon | findstr ":$Port"
        if ($connections) {
            $pids = $connections | ForEach-Object { ($_ -split "\s+")[-1] } | Select-Object -Unique
            foreach ($p in $pids) {
                Write-Host "Stopping process on port $Port (PID $p)..."
                try {
                    taskkill /PID $p /F | Out-Null
                    Write-Host "Process $p terminated."
                } catch {
                    Write-Warning "Could not kill PID $p. Run PowerShell as Administrator."
                }
            }
            Start-Sleep -Seconds 2
        }
    } while ($connections)
}

# ---------- KILL EXISTING BACKEND AND FRONTEND ----------
Write-Host "Stopping any running backend and frontend processes..."

# Kill backend (uvicorn)
Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*uvicorn*" } | ForEach-Object {
    Write-Host "Stopping backend (PID $($_.Id))..."
    Stop-Process -Id $_.Id -Force
}

# Kill frontend (npm/node)
Get-Process -Name "node" -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host "Stopping frontend (PID $($_.Id))..."
    Stop-Process -Id $_.Id -Force
}

# ---------- FREE THE OLLAMA PORT ----------
Write-Host "Ensuring Ollama port $ollamaPort is free..."
Free-Port -Port $ollamaPort

# ---------- START OLLAMA ----------
Write-Host "Starting Ollama in a separate CMD window..."
Start-Process cmd.exe -ArgumentList "/c start cmd /k `"ollama serve`"" -WindowStyle Normal

# Wait briefly for Ollama to start
Start-Sleep -Seconds 5

# Pull AI model if missing
try {
    $modelExists = ollama list | Select-String $modelName
} catch {
    Write-Host "Ollama not responding yet. Waiting a bit..."
    Start-Sleep -Seconds 5
    $modelExists = ollama list | Select-String $modelName
}

if (-not $modelExists) {
    Write-Host "Pulling $modelName..."
    ollama pull $modelName
} else {
    Write-Host "Model $modelName already installed."
}

# ---------- START BACKEND ----------
if (Test-Path $backendPath) {
    Set-Location $backendPath

    # Create venv if missing
    if (!(Test-Path $venvPath)) { python -m venv venv }

    # Activate venv
    .\venv\Scripts\Activate.ps1

    # Install requirements if missing
    if (Test-Path "requirements.txt") { pip install -r requirements.txt }

    # Start backend in a new PowerShell terminal
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "uvicorn app.main:app --reload" -WindowStyle Normal

    Set-Location ..
}

# ---------- START FRONTEND ----------
if (Test-Path $frontendPath) {
    Set-Location $frontendPath

    if (Get-Command npm -ErrorAction SilentlyContinue) {
        # Install dependencies if node_modules doesn't exist
        if (!(Test-Path "node_modules")) { npm install }

        # Start frontend in a new PowerShell terminal
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev" -WindowStyle Normal
    } else {
        Write-Host "npm not installed. Please install Node.js."
    }

    Set-Location ..
}

Write-Host ""
Write-Host "All services restarted successfully!"
Write-Host "- Backend: http://localhost:8000"
Write-Host "- Frontend running in its own terminal"
Write-Host "- Ollama AI running in its own CMD terminal on port $ollamaPort"
