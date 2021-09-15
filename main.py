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
            parser.add_argument("-c", help="Shell handler", type=str)
            args, unknown = parser.parse_known_args()  # The program will ignore all unknown arguments, so type well! #
            # Shell handler #
            if args.c != "" or None:
                arg_len = len(sys.argv)
                argument = str(args.c)
                # Allow Internet Access #
                if "shellHandler.allowAccess" in argument:
                    from src.shellHandler import allowAccess
                    actionLogger("Shell action is allowAccess, allowing...")
                    actionLogger(sys.argv[int(arg_len)-1])
                    allowAccess(sys.argv[int(arg_len)-1], "")
                    sys.exit(0)
                # Deny Internet Access #
                elif "shellHandler.denyAccess" in argument:
                    from src.shellHandler import denyAccess
                    actionLogger("Shell action is denyAccess, blocking...")
                    actionLogger(sys.argv[int(arg_len)-1])
                    denyAccess(sys.argv[int(arg_len)-1], "")
                    sys.exit(0)
            try:
                # Filtering, there's probably a more efficient way to do this #
                toReplace = r"\\"
                replacement = "\\"
                if len(sys.argv) != 1 or len(sys.argv) != 0:
                    try:
                        if "[" and "]" and "'" in str(args.file):
                            file = args.file[2:-2].replace(toReplace, replacement)
                        else:
                            file = args.replace(toReplace, replacement)
                    except AttributeError:
                        if "[" and "]" and "'" in str(args.file):
                            file = args.file[2:-2]
                        else:
                            file = args.file
                else:
                    file = args.file[2:-2].replace(toReplace, replacement)
                # Argument handler #
                file_path = pathlib.Path(file)
                actionLogger(f'Argument "File" is {file}')
                actionLogger(f'Argument "Allow" is {args.allow}')
                if args.allow:
                    actionLogger(f'Attempting to allow "{file_path.stem}"')
                    from src.cmdWorker import allowAccess
                    allowAccess(file_path)
                    sys.exit(0)
                elif not args.allow:
                    actionLogger(f'Attempting to block "{file_path.stem}"')
                    from src.cmdWorker import denyAccess
                    denyAccess(file_path)
                    sys.exit(0)
            except TypeError:
                actionLogger("No variables were caught")

        except argparse.ArgumentTypeError as Argument:
            actionLogger(Argument)
            pass

        # GUI Bootstrap #
        from src.configGui import start
        start()

    except Exception as Critical:
        logException("bypass", Critical)

# Thanks for taking the time to read this script, you nerd \(￣︶￣*\)) #
