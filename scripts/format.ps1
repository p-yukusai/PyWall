#!/usr/bin/env pwsh
# PyWall Format Script
# This script formats code using prettier

param(
    [switch]$Check
)

$basedir = Split-Path $MyInvocation.MyCommand.Definition -Parent
$rootdir = Split-Path $basedir -Parent

$action = if ($Check) { "--check" } else { "--write" }
$actionVerb = if ($Check) { "Checking" } else { "Formatting" }

# Format all files in the project
Write-Host "$actionVerb code..." -ForegroundColor Green
& npx prettier $action "$rootdir/**/*.{py,md,json,yml}"

if ($Check) {
    Write-Host "Code format check completed!" -ForegroundColor Green
} else {
    Write-Host "Code formatting completed!" -ForegroundColor Green
}
