#!/usr/bin/env python3
"""
PyWall - A simple firewall management tool for Windows.
Allows easy control of inbound and outbound connections for applications.
"""

import argparse
import os
import pathlib
import sys

from PyQt5.QtWidgets import QApplication

from src.cmdWorker import access_handler
from src.config import config_exists, document_folder, make_default, validate_config
from src.logger import actionLogger, logException
from src.shellHandler import createInternetAccessMenu, removeInternetAccessMenu


def checkExistingInstall():
    """Check if PyWall is already installed."""
    document_folder_path = document_folder()
    return os.path.exists(document_folder_path + "\\PyWall\\Executable.txt")


def saveCurrentFolder():
    """Save the current folder for context menu access."""
    document_folder_path = document_folder()
    if not os.path.exists(document_folder_path + "\\PyWall"):
        os.makedirs(document_folder_path + "\\PyWall")
    with open(document_folder_path + "\\PyWall\\Executable.txt", 'w') as f:
        f.write(os.path.dirname(os.path.abspath(__file__)))


def main():
    """Main entry point for PyWall."""
    # Verify config file
    if not config_exists():
        make_default()
    if not validate_config():
        make_default()

    parser = argparse.ArgumentParser(
        description='PyWall - Firewall Management Tool')
    parser.add_argument('-file', type=str,
                        help='Target file or directory path')
    parser.add_argument('-allow', type=str,
                        choices=['true', 'True', 'false', 'False'],
                        help='Allow or deny internet access')
    parser.add_argument('-rule_type', type=str,
                        choices=['in', 'out', 'both'],
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
            file_path = sys.argv[3]
            if "allowAccess" in arg[0]:
                action = "allow"
            else:
                action = "deny"
            actionLogger(
                f"Shell action is {arg[0]}, filename is {file_path}, "
                f"rule type is {arg[1]}, proceeding...")
            access_handler(pathlib.Path(file_path), action, arg[1])
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
        # Import and start the GUI
        from src.configGui import start
        app = QApplication(sys.argv)
        try:
            start()  # Use the start function from configGui
        except Exception as e:
            logException("gui_error", e)
            raise
        sys.exit(app.exec_())
    except ImportError as e:
        logException("import_error", e)
        raise
    except Exception as critical:
        logException("unexpected_error", critical)
        raise  # Re-raise the exception after logging it


if __name__ == "__main__":
    main()

# Thanks for taking the time to read this script, you nerd \(￣︶￣*\)) #
