import os
import sys
import ctypes
from pathlib import Path

if len(sys.argv) != 1 or 0:
    from src.pop import toastNotification
else:
    from src.pop import infoMessage, icons, toastNotification
from src.logger import actionLogger, logException
from src.config import getConfig, configFile

ignoredFiles = getConfig("FILETYPE", "blacklisted_names").split(",")


def Admin():
    import ctypes
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin


def pathError(path: Path):
    if not Path.exists(path):
        try:
            icon = icons("critical")
            infoMessage("Path type does not exist", "allTypes is None", "The indicated path does not exist or "
                                                                        "has been incorrectly typed, please try again",
                        icon)
            return
        except NameError:
            actionLogger(f"Commands detected, skipping infoMessage, specified path '{path}' does not exist")
            toastNotification("Path doesn't exist", f'"{str(path.name).title()}" doesn\'t exist or is not a valid '
                                                    f'target please try again.')
            return
    try:
        icon = icons("info")
        infoMessage("No accepted filetype found", "allTypes is None",
                    f'None of the accepted filetypes were found in the suffixes of the files in:\n"{path}"', icon)
        return
    except NameError:
        actionLogger("Commands detected, skipping infoMessage, no accepted filetypes were found")
        toastNotification("No accepted filetypes", f'No file in "{path}" is a valid target, please try again.')
        return


allowedTypeLen = getConfig("FILETYPE", "accepted_types", "len")
allowedTypes = []
for x in range(allowedTypeLen):
    allowedTypes.append(getConfig("FILETYPE", "accepted_types", str(x)))


def path_foreach_in(path):  # A rather telling name, isn't?
    import os
    from glob import glob
    glob_pattern = os.path.join(path, '*')
    filesNoRecursive = sorted(glob(glob_pattern), key=os.path.getctime)
    files = sorted(glob(glob_pattern+r"/**", recursive=True), key=os.path.getctime)
    files = sorted(files + filesNoRecursive, key=os.path.getctime)
    return files


def denyAccess(path: Path):
    allFiles = []
    # And this is what I like to call a double Try incantation! This is unnecessary and just shows bad practice #
    # and as such is perfect for me -w- #
    try:
        try:
            if Path.is_dir(path):
                actionLogger("Folder detected, proceeding accordingly")
                allFiles = []
                for y in path_foreach_in(path):
                    for z in allowedTypes:
                        if z in Path(y).suffix and Path(y).stem not in ignoredFiles:
                            print(Path(y))
                            allFiles.append(Path(y))
            elif Path.is_file(path):
                actionLogger("File detected, proceeding accordingly")
                if Path(path).stem not in ignoredFiles:
                    for z in allowedTypes:
                        if z in Path(path).suffix:
                            allFiles = [path]
        except OSError as rareBug:  # Indeed a rare bug with the context menu, I believe for it to be fixed #
            logException(rareBug)  # but just in case I'll leave this in. #

        if allFiles is None or str(allFiles) == "[]":
            pathError(path)
            return

        for y in allFiles:
            p = Path(y)
            # Yup, this is all the program really does, about 40 hours of coding just to get this to work 〒▽〒 #
            command = f'netsh advfirewall firewall add rule name="PyWall blocked {str(p.stem)}" dir=out program=' \
                      f'"{p}" action=block'
            if Admin():
                os.system(f'cmd /c {command}')
                actionLogger(f"Successfully blocked {str(p.stem)}")
            else:
                try:
                    icon = icons("critical")
                    infoMessage("Not Admin", "Missing required elevation", "This task requires elevation, please run "
                                                                           "as Admin", icon)
                except NameError:
                    actionLogger("Commands detected, skipping infoMessage")
                    pass

                # This code gives me a "held together with spit and glue" kinda vibe #
                args = "".join(sys.argv)
                fileIndex = args.index("-file=")
                args = '"' + args[:fileIndex] + '" ' + args[fileIndex:fileIndex + 6] + '"' + args[fileIndex + 6:]
                ctypes.windll.shell32.ShellExecuteW(None, u"runas", sys.executable, args, None, 1)
                sys.exit("Admin re-run")

    except Exception as Argument:
        logException(Argument)
    if len(sys.argv) != 1 or 0:
        toastNotification("Success", f'Internet access successfully denied to\n"{path}"')
    else:
        toastNotification("Success", f'Internet access successfully denied to\n"{path}"')


def allowAccess(path: Path):
    allFiles = None
    try:
        if Path.is_dir(path):
            actionLogger("Folder detected, proceeding accordingly")
            allFiles = []
            for y in path_foreach_in(path):
                for z in allowedTypes:
                    if z in Path(y).suffix and Path(y).stem not in ignoredFiles:
                        print(Path(y))
                        allFiles.append(Path(y))
        elif Path.is_file(path):
            actionLogger("File detected, proceeding accordingly")
            if Path(path).stem not in ignoredFiles:
                for z in allowedTypes:
                    if z in Path(path).suffix:
                        allFiles = [path]

        if allFiles is None or str(allFiles) == "[]":
            pathError(path)
            return

        for y in allFiles:
            p = Path(y)
            command = f'netsh advfirewall firewall delete rule name="PyWall blocked {str(p.stem)}" dir=out program=' \
                      f'"{p}"'
            if Admin():
                os.system(f'cmd /c {command}')
                actionLogger(f"Successfully allowed {str(p.stem)}")
            else:
                try:
                    icon = icons("critical")
                    infoMessage("Not Admin", "Missing UAC privileges", "This task requires elevation, please run "
                                                                       "as Admin", icon)
                except NameError:
                    actionLogger("Commands detected, skipping infoMessage")
                    pass

                try:
                    args = "".join(sys.argv)
                    fileIndex = args.index("-file=")
                    allowIndex = args.index("-allow")
                    args = '"' + args[:fileIndex] + '" ' + args[fileIndex:fileIndex + 6] + '"' + args[fileIndex + 6:
                                                                                                      allowIndex]\
                           + '" ' + "-" + args[allowIndex + 1:allowIndex + 6] + " " + args[allowIndex + 6:]
                except ValueError:
                    args = "".join(sys.argv)
                ctypes.windll.shell32.ShellExecuteW(None, u"runas", sys.executable, args, None, 1)
                sys.exit("Admin re-run")
    except Exception as Argument:
        logException(Argument)
    if len(sys.argv) != 1 or 0:
        toastNotification("Success", f'Internet access successfully allowed to\n"{path}"')
    else:
        toastNotification("Success", f'Internet access successfully allowed to\n"{path}"')


def openConfig():
    os.system(f'cmd /c {configFile()}')


# For debugging purposes #
def customCommand(command):
    os.system(f'cmd /c {command}')
