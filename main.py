import pathlib
import sys

if __name__ == '__main__':
    from src.logger import logException
    try:
        # Verify config file #
        from src.config import configExists, validateConfig, makeDefault
        if not configExists():
            makeDefault()
        if not validateConfig():
            makeDefault()
        # Argument parser #
        try:
            from src.logger import actionLogger
            import argparse
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
                if "allowAccess" or "denyAccess" in argument:
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
                    access_handler(args.file, "allow", args.rule_type)
                    sys.exit(0)
                elif not args.allow:
                    actionLogger(f'Attempting to block "{file_path.stem}"')
                    access_handler(args.file, "block", args.rule_type)
                    sys.exit(0)

        except argparse.ArgumentTypeError as Argument:
            actionLogger(Argument)
            pass

        # GUI Bootstrap #
        from src.configGui import start
        try:
            start()
        except ValueError:
            start(True)

    except Exception as Critical:
        logException("bypass", Critical)

# Thanks for taking the time to read this script, you nerd \(￣︶￣*\)) #
