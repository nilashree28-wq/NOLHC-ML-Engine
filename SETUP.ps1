# One-time environment setup for the NOLHC ML Engine (Windows PowerShell).
# Builds a virtual environment for each part from its committed lock file.
# Requires Python 3.8.10 (launcher `py -3.8`, or set $env:PYTHON to a python.exe).
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if ($env:PYTHON) { $pyCmd = @($env:PYTHON) } else { $pyCmd = @("py", "-3.8") }

try { & $pyCmd[0] $pyCmd[1..($pyCmd.Length-1)] --version | Out-Null }
catch {
  Write-Error "Python 3.8 not found. Install Python 3.8.10, or set `$env:PYTHON to a python.exe and re-run."
  exit 1
}
Write-Host ("Using " + (& $pyCmd[0] $pyCmd[1..($pyCmd.Length-1)] --version))
Write-Host ""

foreach ($pkg in @("nolhc_ml", "experimenting_ml")) {
  Write-Host "-- $pkg -----------------------------------------------"
  Push-Location $pkg
  & $pyCmd[0] $pyCmd[1..($pyCmd.Length-1)] -m venv .venv
  .\.venv\Scripts\python -m pip install --quiet --upgrade pip
  .\.venv\Scripts\pip install --quiet -r requirements.lock.txt
  Write-Host "  done: $pkg\.venv"
  Pop-Location
  Write-Host ""
}

Write-Host "Setup complete."
Write-Host "  Launch the scenario UI:   .\LAUNCH.ps1"
Write-Host "  Run the tests:            cd nolhc_ml; .\.venv\Scripts\python -m pytest -q"
Write-Host "                            cd ..\experimenting_ml; .\.venv\Scripts\python -m pytest -q"
Write-Host ""
Write-Host "(archive\brexit_ml is superseded and not set up here.)"
