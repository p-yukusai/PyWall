import os
import sys
import ctypes
from pathlib import Path
# I know toasts can be made via PowerShell script, but I cannot be bothered to do so ;) #
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
            return
    try:
        icon = icons("info")
        infoMessage("No accepted filetype found", "allTypes is None",
                    f'None of the accepted filetypes were found in the suffixes of the files in:\n"{path}"', icon)
        return
    except NameError:
        actionLogger("Commands detected, skipping infoMessage, no accepted filetypes were found")
        return


allowedTypeLen = getConfig("FILETYPE", "accepted_types", "len")
allowedTypes = []
for x in range(allowedTypeLen):
    allowedTypes.append(getConfig("FILETYPE", "accepted_types", str(x)))


def path_foreach_in(path):  # A rather telling name, isn't?
    import os
    from glob import glob
    glob_pattern = os.path.join(path, '*')
    files = sorted(glob(glob_pattern), key=os.path.getctime)
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
            logException(rareBug)   # but just in case I'll leave this in. #

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
                    infoMessage("not Admin()", "Missing required elevation", "This task requires elevation, please run "
                                                                             "as Admin", icon)
                except NameError:
                    actionLogger("Commands detected, skipping infoMessage")
                    pass
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                sys.exit("Admin re-run")

    except Exception as Argument:
        logException(Argument)
    if len(sys.argv) != 1 or 0:  # From the GUI the Toast will be threaded, otherwise it won't #
        toastNotification("Success", f"Internet access successfully denied to {path}", 1, False)
    else:
        toastNotification("Success", f"Internet access successfully denied to {path}", 5, True)


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
            print(allFiles)
            command = f'netsh advfirewall firewall delete rule name="PyWall blocked {str(p.stem)}" dir=out program=' \
                      f'"{p}"'
            if Admin():
                os.system(f'cmd /c {command}')
                actionLogger(f"Successfully allowed {str(p.stem)}")
            else:
                try:
                    icon = icons("critical")
                    infoMessage("not Admin()", "Missing UAC privileges", "This task requires elevation, please run "
                                                                         "as Admin", icon)
                except NameError:
                    actionLogger("Commands detected, skipping infoMessage")
                    pass
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                sys.exit("Admin re-run")
    except Exception as Argument:
        logException(Argument)
    if len(sys.argv) != 1 or 0:
        toastNotification("Success", f"Internet access successfully allowed to {path}", 1, False)
    else:
        toastNotification("Success", f"Internet access successfully allowed to {path}", 5, True)


def openConfig():
    os.system(f'cmd /c {configFile()}')


# For debugging purposes #
def customCommand(command):
    os.system(f'cmd /c {command}')
