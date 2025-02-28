#!/usr/bin/env python3
"""
PyWall - A simple firewall management tool for Windows.
Allows easy control of inbound and outbound connections for applications.
"""

import sys
import os
import argparse
from src.cmdWorker import access_handler
from src.config import initConfig, documentFolder, getConfig
from src.shellHandler import createInternetAccessMenu, removeInternetAccessMenu
from src.logger import actionLogger


def checkExistingInstall():
    """Check if PyWall has already saved its location"""
    document_folder = documentFolder()
    script_folder = document_folder + "\\PyWall\\Executable.txt"
    try:
        with open(script_folder, 'r') as sf:
            return True
    except FileNotFoundError:
        return False


def saveCurrentFolder():
    """Save the current folder to allow context menu to find PyWall"""
    document_folder = documentFolder()
    os.makedirs(document_folder + "\\PyWall", exist_ok=True)
    script_folder = document_folder + "\\PyWall\\Executable.txt"
    with open(script_folder, 'w') as sf:
        sf.write(os.path.dirname(os.path.abspath(__file__)))


def main():
    """Main entry point for PyWall"""
    initConfig()

    parser = argparse.ArgumentParser(description='PyWall - Firewall Management Tool')
    parser.add_argument('-file', type=str, help='Target file or directory path')
    parser.add_argument('-allow', type=str, choices=['true', 'True', 'false', 'False'],
                       help='Allow or deny internet access')
    parser.add_argument('-rule_type', type=str, choices=['in', 'out', 'both'],
                       help='Rule type: inbound, outbound, or both')
    parser.add_argument('-install', action='store_true', help='Install context menu')
    parser.add_argument('-uninstall', action='store_true', help='Uninstall context menu')
    parser.add_argument('-config', action='store_true', help='Open configuration file')

    args = parser.parse_args()

    # Save the current folder for context menu access
    if not checkExistingInstall():
        saveCurrentFolder()

    if args.install:
        actionLogger("Installing context menu")
        createInternetAccessMenu()
        return

    if args.uninstall:
        actionLogger("Uninstalling context menu")
        removeInternetAccessMenu()
        return

    if args.config:
        from src.cmdWorker import open_config
        open_config()
        return

    if args.file and args.allow and args.rule_type:
        allow_action = args.allow.lower() == 'true'
        action = "allow" if allow_action else "deny"
        access_handler(args.file, action, args.rule_type)
        return

    # Launch GUI if no command line arguments are provided
    from src.gui import start_gui
    start_gui()


if __name__ == "__main__":
    main()
```python
import pathlib
import sys
import argparse
from PyQt5.QtWidgets import QApplication
from src.logger import logException, actionLogger
from src.config import configExists, validateConfig, makeDefault


class Argument:
    """Simple class to represent argument information for error logging"""
    pass


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='PyWall is a small app to make it easy to administrate '
                                              'simple firewall configurations, giving or revoking internet '
                                              'access to certain applications.')
    # Arguments #
    parser.add_argument("-file", help="The path to the file or folder", type=str)
    parser.add_argument("-allow", help="Action to perform boolean, "
                                    "True will Allow internet access, False will block it.", type=bool)
    parser.add_argument("-rule_type", help="Argument accepts Inbound, outbound or both", type=str)
    parser.add_argument("-c", help="Shell handler", type=str)
    return parser.parse_known_args()


def handle_command_arguments(args, unknown):
    """Handle command line arguments and execute appropriate actions"""
    # Shell handler #
    if args.c is not None:
        argument = str(args.c)
        # Access handling #
        if "allowAccess" in argument or "denyAccess" in argument:
            from src.cmdWorker import access_handler
            arg = argument.split(",")
            file = sys.argv[3]
            if "allowAccess" in arg[0]:
                action = "allow"
            else:
                action = "deny"
            actionLogger(f"Shell action is {arg[0]}, filename is {file}, rule type is {arg[1]}, proceeding...")
            access_handler(pathlib.Path(file), action, arg[1])
            return True

    if args.file is not None and args.allow is not None and args.rule_type is not None:
        # Argument handler #
        file_path = pathlib.Path(str(args.file))
        actionLogger(f'Argument "File" is {file_path}')
        actionLogger(f'Argument "Allow" is {args.allow}')
        actionLogger(f'Argument "Rule type" is {args.rule_type}')
        from src.cmdWorker import access_handler

        if args.allow:
            actionLogger(f'Attempting to allow "{file_path.stem}"')
            access_handler(file_path, "allow", args.rule_type)
            return True
        elif not args.allow:
            actionLogger(f'Attempting to block "{file_path.stem}"')
            access_handler(file_path, "deny", args.rule_type)  # Fixed: Changed "block" to "deny" to match cmdWorker
            return True

    return False


def start_gui():
    """Start the GUI application"""
    from src.configGui import start
    try:
        start()
    except ValueError:
        start(True)


def main():
    """Main entry point for the PyWall application."""
    try:
        # Verify config file #
        if not configExists():
            makeDefault()
        if not validateConfig():
            makeDefault()

        # Parse and handle command line arguments
        try:
            args, unknown = parse_arguments()
            if handle_command_arguments(args, unknown):
                sys.exit(0)
        except argparse.ArgumentTypeError as argument:
            actionLogger(argument)

        # Start GUI if no command line actions were taken
        start_gui()

    # Fix: Replacing the generic Exception with more specific exceptions
    except (ImportError, FileNotFoundError, PermissionError) as critical:
        logException("bypass", critical)
    # If you still need a fallback for truly unexpected errors, use a specific name
    except Exception as critical:  # Catching any other unexpected exceptions
        logException("unexpected_error", critical)
        raise  # Re-raise the exception after logging it


if __name__ == '__main__':
    main()

# Thanks for taking the time to read this script, you nerd \(￣︶￣*\)) #
