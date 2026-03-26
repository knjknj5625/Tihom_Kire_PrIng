$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$logsDir = Join-Path $projectRoot "logs"

New-Item -ItemType Directory -Force -Path $logsDir | Out-Null

$fastapiOut = Join-Path $logsDir "fastapi.out.log"
$fastapiErr = Join-Path $logsDir "fastapi.err.log"
$streamlitOut = Join-Path $logsDir "streamlit.out.log"
$streamlitErr = Join-Path $logsDir "streamlit.err.log"

Write-Host "Logs directory: $logsDir"

Start-Process python `
    -ArgumentList @("-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000") `
    -WorkingDirectory $projectRoot `
    -RedirectStandardOutput $fastapiOut `
    -RedirectStandardError $fastapiErr

Start-Process python `
    -ArgumentList @("-m", "streamlit", "run", "streamlit_app.py", "--server.headless", "true", "--server.address", "127.0.0.1", "--server.port", "8501") `
    -WorkingDirectory $projectRoot `
    -RedirectStandardOutput $streamlitOut `
    -RedirectStandardError $streamlitErr

Write-Host "FastAPI and Streamlit started."
