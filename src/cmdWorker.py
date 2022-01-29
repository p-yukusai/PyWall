import subprocess
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
        if path.is_dir():
            toastNotification("No accepted filetypes", f'No file in\n"{path}"\nis a valid target, please try again.')
        else:
            toastNotification("Filetype not accepted", f'Suffix "{path.suffix}" in file "{path.name}" is not a valid'
                                                       f' target, please try again')
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
    if getConfig("FILETYPE", "recursive") == "True":
        filesRecursive = sorted(glob(glob_pattern+r"/**", recursive=True), key=os.path.getctime)
        files = sorted(filesRecursive + filesNoRecursive, key=os.path.getctime)
    elif getConfig("FILETYPE", "recursive") == "False":
        files = filesNoRecursive
    else:
        from src.config import modifyConfig
        modifyConfig("FILETYPE", "recursive", "True")
        filesRecursive = sorted(glob(glob_pattern+r"/**", recursive=True), key=os.path.getctime)
        files = sorted(filesRecursive + filesNoRecursive, key=os.path.getctime)
    return files

def access_handler(path: Path, action):
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
            if action == "block":
                command = f'@echo off && netsh advfirewall firewall add rule name="PyWall blocked {str(p.stem)}" ' \
                          f'dir=out program="{p}" action=block'
            elif action == "allow":
                command = f'@echo off && netsh advfirewall firewall delete rule name="PyWall blocked {str(p.stem)}" ' \
                          f'dir=out program="{p}"'
            else:
                return "Invalid action"

            if Admin():
                subprocess.call(f'cmd /c {command}', shell=True)
                actionLogger(f"Successfully blocked {str(p.stem)}")
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
                                                                                                      allowIndex] \
                           + '" ' + "-" + args[allowIndex + 1:allowIndex + 6] + " " + args[allowIndex + 6:]
                except ValueError:
                    args = "".join(sys.argv)
                ctypes.windll.shell32.ShellExecuteW(None, u"runas", sys.executable, args, None, 1)
                sys.exit("Admin re-run")

    except Exception as Argument:
        logException(Argument)
    if action == "block":
        toastNotification("Success", f'Internet access successfully denied to\n"{path}"')
    elif action == "allow":
        toastNotification("Success", f'Internet access successfully allowed to\n"{path}"')
    else:
        return "Invalid action"


def openConfig():
    subprocess.call(f'cmd /c @echo off && {configFile()}')


# For debugging purposes #
def customCommand(command):
    subprocess.call(f'cmd /c @echo off & {command}')
