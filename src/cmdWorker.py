"""
cmdWorker module for handling firewall rules.
"""

import subprocess
import os
import sys
import ctypes
import pathlib
from src.pop import toastNotification, infoMessage, icons
from src.logger import actionLogger, logException
from src.config import getConfig, config_file as configFile

ignoredFiles = getConfig("FILETYPE", "blacklisted_names").split(",")


def admin():
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin


def path_error(path: pathlib.Path):
    if not pathlib.Path.exists(path):
        try:
            icon = icons("critical")
            infoMessage(
                "Path type does not exist",
                "allTypes is None",
                "The indicated path does not exist or "
                "has been incorrectly typed, please try again",
                icon
            )
            return
        except NameError:
            actionLogger(
                f"Commands detected, skipping infoMessage, specified path '{path}' does not exist")
            toastNotification(
                "Path doesn't exist",
                f'"{str(path.name).title()}" doesn\'t exist or is not a valid '
                f'target please try again.'
            )
            return
    try:
        icon = icons("info")
        infoMessage(
            "No accepted filetype found",
            "allTypes is None",
            f'None of the accepted filetypes were found in the suffixes of the files in:\n"{path}"',
            icon
        )
        return
    except NameError:
        actionLogger(
            "Commands detected, skipping infoMessage, no accepted filetypes were found")
        if path.is_dir():
            toastNotification(
                "No accepted filetypes",
                f'No file in\n"{path}"\nis a valid target, please try again.'
            )
        else:
            toastNotification(
                "Filetype not accepted",
                f'Suffix "{path.suffix}" in file "{path.name}" is not a valid'
                f' target, please try again'
            )
        return


def get_allowed_types():
    allowed_types_str = getConfig("FILETYPE", "accepted_types")
    if not allowed_types_str:
        return []
    return [t.strip() for t in allowed_types_str.split(",")]


allowedTypes = get_allowed_types()


def path_foreach_in(path):  # A rather telling name, isn't?
    from glob import glob
    glob_pattern = os.path.join(path, '*')
    filesNoRecursive = sorted(glob(glob_pattern), key=os.path.getctime)
    if getConfig("FILETYPE", "recursive") == "True":
        filesRecursive = sorted(
            glob(glob_pattern + r"/**", recursive=True), key=os.path.getctime)
        files = sorted(filesRecursive + filesNoRecursive, key=os.path.getctime)
    elif getConfig("FILETYPE", "recursive") == "False":
        files = filesNoRecursive
    else:
        from src.config import modifyConfig
        modifyConfig("FILETYPE", "recursive", "True")
        filesRecursive = sorted(
            glob(glob_pattern + r"/**", recursive=True), key=os.path.getctime)
        files = sorted(filesRecursive + filesNoRecursive, key=os.path.getctime)
    return files


def access_handler(path, action, rule_type: str):
    allFiles = None

    if rule_type not in {"both", "in", "out"}:
        from src.shellHandler import pop
        pop(
            "Rule type is invalid",
            f"The selected rule type ('{rule_type}') is not valid, please try again",
            True
        )
        return

    try:
        path = pathlib.Path(str(path).strip())
        is_dir = path.is_dir()
        is_file = path.is_file()
        if is_dir:
            actionLogger("Folder detected, proceeding accordingly")
            allFiles = [
                pathlib.Path(y) for y in path_foreach_in(path)
                if any(z in pathlib.Path(y).suffix for z in allowedTypes)
                and pathlib.Path(y).stem not in ignoredFiles
            ]
        elif is_file:
            actionLogger("File detected, proceeding accordingly")
            if pathlib.Path(path).stem not in ignoredFiles:
                if any(z in pathlib.Path(path).suffix for z in allowedTypes):
                    allFiles = [path]
    except OSError:
        path_error(path)
        return

    if not allFiles:
        path_error(path)
        return

    try:
        for y in allFiles:
            p = pathlib.Path(y)
            command = False
            if action == "deny":
                cmn = "blocked"
                if rule_type != "both":
                    command = (
                        f'@echo off && netsh advfirewall firewall add rule name="PyWall blocked {str(p.stem)}" '
                        f'dir={rule_type} program="{p}" action=block'
                    )
            else:
                cmn = "allowed"
                if rule_type != "both":
                    command = (
                        f'@echo off && netsh advfirewall firewall delete rule name="PyWall blocked {str(p.stem)}" '
                        f'dir={rule_type} program="{p}"'
                    )

            if admin():
                if not command and action == "allow":
                    first_command = (
                        f'@echo off && netsh advfirewall firewall delete rule name="PyWall blocked '
                        f'{str(p.stem)}" dir=out program="{p}"'
                    )
                    second_command = (
                        f'@echo off && netsh advfirewall firewall delete rule name="PyWall blocked '
                        f'{str(p.stem)}" dir=in program="{p}"'
                    )
                    subprocess.call(f'cmd /c {first_command}', shell=True)
                    subprocess.call(f'cmd /c {second_command}', shell=True)
                elif not command and action == "deny":
                    first_command = (
                        f'@echo off && netsh advfirewall firewall add rule name="PyWall blocked '
                        f'{str(p.stem)}" dir=out program="{p}" action=block'
                    )
                    second_command = (
                        f'@echo off && netsh advfirewall firewall add rule name="PyWall blocked '
                        f'{str(p.stem)}" dir=in program="{p}" action=block'
                    )
                    subprocess.call(f'cmd /c {first_command}', shell=True)
                    subprocess.call(f'cmd /c {second_command}', shell=True)
                else:
                    subprocess.call(f'cmd /c {command}', shell=True)
                actionLogger(f"Successfully {cmn} {str(p.stem)}")
            else:
                try:
                    icon = icons("critical")
                    infoMessage(
                        "Not Admin",
                        "Missing UAC privileges",
                        "This task requires elevation, please run as Admin",
                        icon
                    )
                except NameError:
                    actionLogger("Commands detected, skipping infoMessage")
                    pass
                # Fixed bug: Changed from "".join(sys.argv) to " ".join(sys.argv)
                args = " ".join(sys.argv)
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, args, None, 1)
            sys.exit("Admin re-run")

    except Exception as argument:
        logException(argument)  # Fixed: Changed from Argument to argument
        raise

    if action == "deny":
        toastNotification(
            "Success", f'Internet access successfully denied to\n"{path}"')
    elif action == "allow":
        toastNotification(
            "Success", f'Internet access successfully allowed to\n"{path}"')
    else:
        return "Invalid action"


def open_config():
    subprocess.call(f'cmd /c @echo off && {configFile()}')
