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
