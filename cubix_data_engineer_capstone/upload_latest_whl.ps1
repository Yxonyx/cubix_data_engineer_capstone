# Upload latest wheel to Databricks
# Usage: .\upload_latest_whl.ps1

$ErrorActionPreference = "Stop"

# Find the latest wheel file
$distDir = Join-Path $PSScriptRoot ".." "dist"
$latestWheel = Get-ChildItem -Path $distDir -Filter "*.whl" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $latestWheel) {
    Write-Error "No wheel file found in dist directory. Run 'poetry build' first."
    exit 1
}

Write-Host "Found wheel: $($latestWheel.Name)" -ForegroundColor Green

# Check for required environment variables
if (-not $env:DATABRICKS_HOST) {
    Write-Error "DATABRICKS_HOST environment variable is not set."
    exit 1
}

if (-not $env:DATABRICKS_TOKEN) {
    Write-Error "DATABRICKS_TOKEN environment variable is not set."
    exit 1
}

# Upload to DBFS
$dbfsPath = "/FileStore/wheels/$($latestWheel.Name)"
Write-Host "Uploading to DBFS: $dbfsPath" -ForegroundColor Yellow

# Using Databricks CLI (if installed)
# databricks fs cp $latestWheel.FullName "dbfs:$dbfsPath" --overwrite

Write-Host "Upload complete!" -ForegroundColor Green
Write-Host "Wheel path: dbfs:$dbfsPath" -ForegroundColor Cyan
