$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$logsDir = Join-Path $projectRoot "logs"

New-Item -ItemType Directory -Force -Path $logsDir | Out-Null

$stdoutLog = Join-Path $logsDir "streamlit.out.log"
$stderrLog = Join-Path $logsDir "streamlit.err.log"

Write-Host "Streamlit logs:"
Write-Host "  stdout -> $stdoutLog"
Write-Host "  stderr -> $stderrLog"

& python -m streamlit run streamlit_app.py --server.headless true --server.address 127.0.0.1 --server.port 8501 1>> $stdoutLog 2>> $stderrLog
