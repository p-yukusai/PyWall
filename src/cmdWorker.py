import subprocess
import os
import sys
import ctypes
import pathlib

if len(sys.argv) != 1 or len(sys.argv) != 0:
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


def pathError(path: pathlib.Path):
    if not pathlib.Path.exists(path):
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
        filesRecursive = sorted(glob(glob_pattern + r"/**", recursive=True), key=os.path.getctime)
        files = sorted(filesRecursive + filesNoRecursive, key=os.path.getctime)
    elif getConfig("FILETYPE", "recursive") == "False":
        files = filesNoRecursive
    else:
        from src.config import modifyConfig
        modifyConfig("FILETYPE", "recursive", "True")
        filesRecursive = sorted(glob(glob_pattern + r"/**", recursive=True), key=os.path.getctime)
        files = sorted(filesRecursive + filesNoRecursive, key=os.path.getctime)
    return files

def access_handler(path, action, rule_type: str):
    allFiles = None

    if rule_type != "both" and rule_type != "in" and rule_type != "out":
        from src.shellHandler import pop
        pop("Rule type is invalid", f"The selected rule type ('{rule_type}') is not valid, please"
            f"try again", True)
        return

    try:
        try:
            # I have NO idea why it adds a random space at the start of the path, this was a headache during
            # debugging ;w;
            path = pathlib.Path(str(path).strip())
            is_dir = bool(path.is_dir())
            is_file = bool(path.is_file())
            if is_dir:
                actionLogger("Folder detected, proceeding accordingly")
                allFiles = []
                for y in path_foreach_in(path):
                    for z in allowedTypes:
                        if z in pathlib.Path(y).suffix and pathlib.Path(y).stem not in ignoredFiles:
                            print(pathlib.Path(y))
                            allFiles.append(pathlib.Path(y))
            elif is_file:
                actionLogger("File detected, proceeding accordingly")
                if pathlib.Path(path).stem not in ignoredFiles:
                    for z in allowedTypes:
                        if z in pathlib.Path(path).suffix:
                            allFiles = [path]
        except OSError:
            raise pathError(path)

        if allFiles is None or str(allFiles) == "[]":
            pathError(path)
            return

        for y in allFiles:
            p = pathlib.Path(y)
            command = False
            if action == "deny":
                cmn = "blocked"
                if rule_type != "both":
                    command = f'@echo off && netsh advfirewall firewall add rule name="PyWall blocked {str(p.stem)}" ' \
                              f'dir={rule_type} program="{p}" action=block'
            else:
                cmn = "allowed"
                if rule_type != "both":
                    command = f'@echo off && netsh advfirewall firewall delete rule name="PyWall blocked {str(p.stem)}" ' \
                              f'dir={rule_type} program="{p}"'

            if Admin():
                if not command and action == "allow":
                    first_command = f'@echo off && netsh advfirewall firewall delete rule name="PyWall blocked ' \
                                    f'{str(p.stem)}" dir=out program="{p}"'
                    second_command = f'@echo off && netsh advfirewall firewall delete rule name="PyWall blocked ' \
                                    f'{str(p.stem)}" dir=in program="{p}"'
                    subprocess.call(f'cmd /c {first_command}', shell=True)
                    subprocess.call(f'cmd /c {second_command}', shell=True)
                elif not command and action == "deny":
                    first_command = f'@echo off && netsh advfirewall firewall add rule name="PyWall blocked ' \
                                    f'{str(p.stem)}" dir=out program="{p}" action=block'
                    second_command = f'@echo off && netsh advfirewall firewall add rule name="PyWall blocked ' \
                                     f'{str(p.stem)}" dir=in program="{p}" action=block'
                    subprocess.call(f'cmd /c {first_command}', shell=True)
                    subprocess.call(f'cmd /c {second_command}', shell=True)
                else:
                    subprocess.call(f'cmd /c {command}', shell=True)
                actionLogger(f"Successfully {cmn} {str(p.stem)}")
            else:
                try:
                    icon = icons("critical")
                    infoMessage("Not Admin", "Missing UAC privileges", "This task requires elevation, please run "
                                                                       "as Admin", icon)
                except NameError:
                    actionLogger("Commands detected, skipping infoMessage")
                    pass
                args = "".join(sys.argv)
                ctypes.windll.shell32.ShellExecuteW(None, u"runas", sys.executable, args, None, 1)
                sys.exit("Admin re-run")

    except Exception as Argument:
        logException(Argument)
        raise Argument
    if action == "deny":
        toastNotification("Success", f'Internet access successfully denied to\n"{path}"')
    elif action == "allow":
        toastNotification("Success", f'Internet access successfully allowed to\n"{path}"')
    else:
        return "Invalid action"


def openConfig():
    subprocess.call(f'cmd /c @echo off && {configFile()}')
