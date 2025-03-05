# PyWall Scripts

This directory contains utility scripts for PyWall development and deployment.

## Available Scripts

### build.ps1

PowerShell script to build PyWall using PyInstaller.

Usage:

```powershell
# Build with no console window (default)
./scripts/build.ps1

# Build with console window for debugging
./scripts/build.ps1 -ShowConsole
```

This script:

1. Installs dependencies using pipenv
2. Activates the virtual environment
3. Builds the application with PyInstaller
4. Creates an executable in the dist/PyWall directory

Parameters:

- `-ShowConsole`: When specified, builds PyWall with a console window for debugging

### format.ps1

PowerShell script to format code using prettier.

Usage:

```powershell
# Format code
./scripts/format.ps1

# Check code formatting without making changes
./scripts/format.ps1 -Check
```

This script formats all Python, Markdown, JSON, and YAML files in the project using prettier.

Parameters:

- `-Check`: When specified, checks formatting without making changes

### update_version.ps1

PowerShell script to update the version number across all relevant files.

Usage:

```powershell
./scripts/update_version.ps1 -NewVersion "0.9.1"
```

This script updates the version number in:

1. setup.py
2. package.json
3. PyWall Installer.iss
4. src/config.py

## Adding New Scripts

When adding new scripts to this directory, please follow these guidelines:

1. Use descriptive names for your scripts
2. Include a shebang line at the top of the script
3. Add proper documentation within the script
4. Update this README with information about the new script
