#!/usr/bin/env pwsh
# PyWall Build Script
# This script builds PyWall using PyInstaller

param(
    [switch]$ShowConsole
)

# Ensure dependencies are installed
Write-Host "Installing dependencies..." -ForegroundColor Green
pipenv sync -d

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
$env:PIPENV_VENV_IN_PROJECT = "true"
$venvPath = & pipenv --venv

# Build the application
Write-Host "Building PyWall..." -ForegroundColor Green

$windowParam = if (-not $ShowConsole) { "--windowed" } else { "" }

cd ..
pipenv run pyinstaller "main.py" --noconfirm --onedir --uac-admin -n "PyWall" --icon "img/PyWall.ico" $windowParam  --contents-directory . --add-data "img;img/" --add-data "src;src/" --add-data "$venvPath\Lib\site-packages\context_menu;context_menu/"

Write-Host "Build completed successfully!" -ForegroundColor Green
Write-Host "The executable can be found in the dist/PyWall directory." -ForegroundColor Cyan
