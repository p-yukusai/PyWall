#!/usr/bin/env pwsh
# PyWall Version Update Script
# This script updates the version number across all relevant files

param(
    [Parameter(Mandatory=$true)]
    [string]$NewVersion
)

$basedir = Split-Path $MyInvocation.MyCommand.Definition -Parent
$rootdir = Split-Path $basedir -Parent

# Files to update
$setupPy = Join-Path $rootdir "setup.py"
$packageJson = Join-Path $rootdir "package.json"
$installerIss = Join-Path $rootdir "PyWall Installer.iss"
$configPy = Join-Path $rootdir "src\config.py"

Write-Host "Updating PyWall version to $NewVersion..." -ForegroundColor Green

# Update setup.py
if (Test-Path $setupPy) {
    $content = Get-Content $setupPy -Raw
    $updatedContent = $content -replace 'version="[0-9]+\.[0-9]+\.[0-9]+"', "version=`"$NewVersion`""
    Set-Content -Path $setupPy -Value $updatedContent
    Write-Host "Updated setup.py" -ForegroundColor Cyan
}

# Update package.json
if (Test-Path $packageJson) {
    $content = Get-Content $packageJson -Raw
    $updatedContent = $content -replace '"version": "[0-9]+\.[0-9]+\.[0-9]+"', "`"version`": `"$NewVersion`""
    Set-Content -Path $packageJson -Value $updatedContent
    Write-Host "Updated package.json" -ForegroundColor Cyan
}

# Update PyWall Installer.iss
if (Test-Path $installerIss) {
    $content = Get-Content $installerIss -Raw
    $updatedContent = $content -replace '#define MyAppVersion "[^"]+"', "#define MyAppVersion `"$NewVersion`""
    Set-Content -Path $installerIss -Value $updatedContent
    Write-Host "Updated PyWall Installer.iss" -ForegroundColor Cyan
}

# Update src/config.py
if (Test-Path $configPy) {
    $content = Get-Content $configPy -Raw
    $updatedContent = $content -replace '"version": "v[0-9]+\.[0-9]+\.[0-9]+"', "`"version`": `"v$NewVersion`""
    Set-Content -Path $configPy -Value $updatedContent
    Write-Host "Updated src/config.py" -ForegroundColor Cyan
}

Write-Host "Version update completed successfully!" -ForegroundColor Green
Write-Host "PyWall is now at version $NewVersion" -ForegroundColor Green
