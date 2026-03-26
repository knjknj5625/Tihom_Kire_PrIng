$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$logsDir = Join-Path $projectRoot "logs"

New-Item -ItemType Directory -Force -Path $logsDir | Out-Null

$stdoutLog = Join-Path $logsDir "fastapi.out.log"
$stderrLog = Join-Path $logsDir "fastapi.err.log"

Write-Host "FastAPI logs:"
Write-Host "  stdout -> $stdoutLog"
Write-Host "  stderr -> $stderrLog"

& python -m uvicorn main:app --host 127.0.0.1 --port 8000 1>> $stdoutLog 2>> $stderrLog
