import pathlib
import sys
from src.logger import logException, actionLogger  # Moved to the top
from src.config import configExists, validateConfig, makeDefault
import argparse

if __name__ == '__main__':
    try:
        # Verify config file #
        if not configExists():
            makeDefault()
        if not validateConfig():
            makeDefault()
        # Argument parser #
        try:
            parser = argparse.ArgumentParser(description='PyWall is a small app to make it easy to administrate '
                                                         'simple firewall configurations, giving or revoking internet '
                                                         'access to certain applications.')
            # Arguments #
            parser.add_argument("-file", help="The path to the file or folder", type=str)
            parser.add_argument("-allow", help="Action to perform boolean, "
                                               "True will Allow internet access, False will block it.", type=bool)
            parser.add_argument("-rule_type", help="Argument accepts Inbound, outbound or both", type=str)
            parser.add_argument("-c", help="Shell handler", type=str)
            args, unknown = parser.parse_known_args()  # The program will ignore all unknown arguments, so type well! #
            # Shell handler #
            if args.c is not None:
                argument = str(args.c)
                # Access handling #
                # FIX: Corrected the logical condition that was always evaluating to True
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
                    sys.exit(0)
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
                    sys.exit(0)
                elif not args.allow:
                    actionLogger(f'Attempting to block "{file_path.stem}"')
                    access_handler(file_path, "block", args.rule_type)
                    sys.exit(0)

        except argparse.ArgumentTypeError as Argument:
            actionLogger(Argument)

        # GUI Bootstrap #
        from src.configGui import start
        try:
            start()
        except ValueError:
            start(True)

    # Fix: Replacing the generic Exception with more specific exceptions
    except (ImportError, FileNotFoundError, PermissionError) as Critical:
        logException("bypass", Critical)
    # If you still need a fallback for truly unexpected errors, use a specific name
    except Exception as Critical:  # Catching any other unexpected exceptions
        logException("unexpected_error", Critical)
        raise  # Re-raise the exception after logging it

# Thanks for taking the time to read this script, you nerd \(￣︶￣*\)) #
