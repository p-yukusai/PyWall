#!/usr/bin/env pwsh
# PyWall Deploy Script
# This script builds PyWall and packages it using Inno Setup, it assumes default install location

Write-Host "Running build script" -ForegroundColor Magenta
& "$PSScriptRoot\build.ps1"
Write-Host "Build script completed, deploying..." -ForegroundColor Magenta

$RootPath = Split-Path $PSScriptRoot -Parent
Start-Process "C:\Program Files (x86)\Inno Setup 6\Compil32.exe" -ArgumentList "/cc ""$RootPath\PyWall Installer.iss"""
Wait-Process -Name "Compil32" -Timeout 60

Write-Host "Deployment completed successfully!" -ForegroundColor Magenta
Start-Process "explorer" -ArgumentList "$RootPath\Output"