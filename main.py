#!/usr/bin/env python3
"""
PyWall - A simple firewall management tool for Windows.
Allows easy control of inbound and outbound connections for applications.
"""

from src.config import initConfig, documentFolder, getConfig, configExists, validateConfig, makeDefault
from src.logger import logException, actionLogger
from PyQt5.QtWidgets import QApplication
import pathlib
import sys
import os
import argparse
from src.cmdWorker import access_handler
from src.shellHandler import createInternetAccessMenu, removeInternetAccessMenu


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


class Argument:
    """Simple class to represent argument information for error logging"""
    pass


def main():
    """Main entry point for PyWall"""
    # Verify config file
    if not configExists():
        makeDefault()
    if not validateConfig():
        makeDefault()

    initConfig()

    parser = argparse.ArgumentParser(
        description='PyWall - Firewall Management Tool')
    parser.add_argument('-file', type=str,
                        help='Target file or directory path')
    parser.add_argument('-allow', type=str, choices=['true', 'True', 'false', 'False'],
                        help='Allow or deny internet access')
    parser.add_argument('-rule_type', type=str, choices=['in', 'out', 'both'],
                        help='Rule type: inbound, outbound, or both')
    parser.add_argument('-install', action='store_true',
                        help='Install context menu')
    parser.add_argument('-uninstall', action='store_true',
                        help='Uninstall context menu')
    parser.add_argument('-config', action='store_true',
                        help='Open configuration file')
    parser.add_argument("-c", help="Shell handler", type=str)

    args = parser.parse_args()

    # Save the current folder for context menu access
    if not checkExistingInstall():
        saveCurrentFolder()

    # Shell handler
    if args.c is not None:
        argument = str(args.c)
        # Access handling
        if "allowAccess" in argument or "denyAccess" in argument:
            arg = argument.split(",")
            file = sys.argv[3]
            if "allowAccess" in arg[0]:
                action = "allow"
            else:
                action = "deny"
            actionLogger(
                f"Shell action is {arg[0]}, filename is {file}, rule type is {arg[1]}, proceeding...")
            access_handler(pathlib.Path(file), action, arg[1])
            return

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
        file_path = pathlib.Path(str(args.file))
        actionLogger(f'Argument "File" is {file_path}')
        actionLogger(f'Argument "Allow" is {allow_action}')
        actionLogger(f'Argument "Rule type" is {args.rule_type}')

        if allow_action:
            actionLogger(f'Attempting to allow "{file_path.stem}"')
        else:
            actionLogger(f'Attempting to block "{file_path.stem}"')

        access_handler(file_path, action, args.rule_type)
        return

    # Launch GUI if no command line arguments are provided
    try:
        from src.gui import start_gui
        start_gui()
    except Exception as critical:
        logException("unexpected_error", critical)
        raise  # Re-raise the exception after logging it


if __name__ == "__main__":
    main()

# Thanks for taking the time to read this script, you nerd \(￣︶￣*\)) #
