# Start the NOLHC ML Engine's primary interface: the scenario
# Decision-Intelligence UI (predictions + uncertainty + SHAP + operator
# console). Windows PowerShell. Run .\SETUP.ps1 first if you haven't.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$port = if ($env:PORT) { $env:PORT } else { "8000" }
$venv = "experimenting_ml\.venv\Scripts\python.exe"

if (-not (Test-Path $venv)) {
  Write-Error "$venv not found. Run .\SETUP.ps1 first."
  exit 1
}

Write-Host "Scenario UI:         http://localhost:$port/UI/index.html"
Write-Host "Settings / operator: http://localhost:$port/UI/settings.html"
Write-Host "(Ctrl-C to stop.)"
Write-Host ""

Set-Location experimenting_ml
& ".\.venv\Scripts\python" run_ui_inference_api.py --port $port
