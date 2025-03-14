import os
import pathlib
import subprocess
import sys  # Added missing sys import at the module level

from context_menu import menus

from src.config import document_folder
from src.pop import toastNotification


# Having to define stuff anew in this script, since it's technically separate in the context of the shell
# this means duping already existing code :(


def getScriptFolder():
    document_folder_path = str(document_folder())
    return document_folder_path + "\\PyWall\\Executable.txt"

def pop(title, text, close: bool):
    toastNotification(title, text)
    if close:
        sys.exit(0)


# The "open" command is repeated because I'm too lazy to define it and then just call it later, code redundancy go brr #
def pyWallPath(folder):
    return pathlib.Path(str(folder) + "/PyWall.exe")


def pyWallScript(folder):
    return pathlib.Path(str(folder) + "/main.py")


def getFolder():
    try:
        with open(getScriptFolder(), 'r') as sf:
            folder = sf.read()
            return folder
    except FileNotFoundError:
        pop("PyWall.exe not found",
            "Could not find PyWall, please open the program and try again.", True)


def allowAccess(filenames, params):
    folder = getFolder()
    try:
        if pyWallPath(folder).is_file() or pyWallScript(folder).is_file():
            subprocess.call(
                f'cmd /c cd "{folder}" && PyWall.exe -file "{filenames}" -allow true -rule_type {params}', shell=True)
            # input() #
            subprocess.call(
                f'cmd /c cd "{folder}" && python "{folder}\\main.py" -file "{filenames}" -allow true -rule_type {params}', shell=True)
            # input() #
        else:
            os.remove(getScriptFolder())
            pop("PyWall.exe not found",
                "Could not find PyWall, please open the program and try again.", True)
    except FileNotFoundError:
        pop("PyWall.exe not found",
            "Could not find PyWall, please open the program and try again.", True)


def denyAccess(filenames, params):
    folder = getFolder()
    try:
        if pyWallPath(folder).is_file() or pyWallScript(folder).is_file():
            subprocess.call(
                f'cmd /c cd "{folder}" && PyWall.exe -file "{filenames}" -allow false -rule_type {params}', shell=True)
            # input() #
            subprocess.call(
                f'cmd /c cd "{folder}" && python "{folder}\\main.py" -file "{filenames}" -allow false -rule_type {params}', shell=True)
            # input() #
        else:
            os.remove(getScriptFolder())
            pop("PyWall.exe not found",
                "Could not find PyWall, please open the program and try again.", True)
    except FileNotFoundError:
        pop("PyWall.exe not found",
            "Could not find PyWall, please open the program and try again.", True)


# This creates the context menu, It is important to do this for FILES and for DIRECTORY so that the user can right #
# click on either. The keys created are in "HKEY_CURRENT_USER\Software\Classes\*\shell\" for FILES and in #
# "HKEY_CURRENT_USER\Software\Classes\Directory\shell" for DIRECTORY #

def createInternetAccessMenu():
    IAM = menus.ContextMenu('PyWall', type='FILES')
    IAM_ALLOW = createAllowMenu()
    IAM_DENY = createDenyMenu()
    IAM.add_items([IAM_ALLOW, IAM_DENY])
    IAM.compile()

    IAM_Folder = menus.ContextMenu('PyWall', type='DIRECTORY')
    IAM_Folder.add_items([IAM_ALLOW, IAM_DENY])
    IAM_Folder.compile()

    updateRegistry()


def createAllowMenu():
    IAM_ALLOW = menus.ContextMenu('Allow Internet Access')
    IAM_ALLOW.add_items([
        menus.ContextCommand("Allow inbound connections",
                             python=allowAccess, params='in'),
        menus.ContextCommand("Allow outbound connections",
                             python=allowAccess, params="out"),
        menus.ContextCommand(
            "Allow inbound and outbound connections", python=allowAccess, params="both")
    ])
    return IAM_ALLOW


def createDenyMenu():
    IAM_DENY = menus.ContextMenu('Deny Internet Access')
    IAM_DENY.add_items([
        menus.ContextCommand("Deny inbound connections",
                             python=denyAccess, params='in'),
        menus.ContextCommand("Deny outbound connections",
                             python=denyAccess, params="out"),
        menus.ContextCommand(
            "Deny inbound and outbound connections", python=denyAccess, params="both")
    ])
    return IAM_DENY


def updateRegistry():
    import winreg
    # Command registry #
    # Yes, this was just as tedious as you think it was #
    FILES_ALLOW_BOTH = r"Software\Classes\*\shell\PyWall\shell\Allow Internet Access\shell\Allow inbound " \
                       r"and outbound connections\command"
    FILES_ALLOW_IN = r"Software\Classes\*\shell\PyWall\shell\Allow Internet Access\shell\Allow inbound " \
                     r"connections\command"
    FILES_ALLOW_OUT = r"Software\Classes\*\shell\PyWall\shell\Allow Internet Access\shell\Allow outbound " \
                      r"connections\command"
    FILES_DENY_BOTH = r"Software\Classes\*\shell\PyWall\shell\Deny Internet Access\shell\Deny inbound " \
                      r"and outbound connections\command"
    FILES_DENY_IN = r"Software\Classes\*\shell\PyWall\shell\Deny Internet Access\shell\Deny inbound " \
                    r"connections\command"
    FILES_DENY_OUT = r"Software\Classes\*\shell\PyWall\shell\Deny Internet Access\shell\Deny outbound " \
                     r"connections\command"
    # ---- #
    DIR_ALLOW_BOTH = FILES_ALLOW_BOTH.replace("*", "Directory")
    DIR_ALLOW_IN = FILES_ALLOW_IN.replace("*", "Directory")
    DIR_ALLOW_OUT = FILES_ALLOW_OUT.replace("*", "Directory")
    DIR_DENY_BOTH = FILES_DENY_BOTH.replace("*", "Directory")
    DIR_DENY_IN = FILES_DENY_IN.replace("*", "Directory")
    DIR_DENY_OUT = FILES_DENY_OUT.replace("*", "Directory")

    key = winreg.HKEY_CURRENT_USER
    sub_keys = [
        FILES_ALLOW_BOTH, FILES_DENY_BOTH, FILES_ALLOW_IN, FILES_DENY_IN, FILES_ALLOW_OUT, FILES_DENY_OUT,
        DIR_ALLOW_BOTH, DIR_DENY_BOTH, DIR_ALLOW_IN, DIR_DENY_IN, DIR_ALLOW_OUT, DIR_DENY_OUT
    ]

    # Icon registry #
    PYWALL_REG_FILE = r"Software\Classes\*\shell\PyWall"
    PYWALL_REG_FOLDER = r"Software\Classes\Directory\shell\PyWall"

    try:
        # This key will only work if run from an executable, and not if it is run from source #
        folder = getFolder()
        try:
            PYWALL_KEY = winreg.OpenKey(
                key, PYWALL_REG_FILE, 0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(PYWALL_KEY, 'Icon', 0, winreg.REG_SZ,
                              str(pyWallPath(folder)) + ",0")
            winreg.CloseKey(PYWALL_KEY)
        except Exception as e:
            print(f"Warning: Could not set file icon: {e}")

        try:
            PYWALL_FOLDER_KEY = winreg.OpenKey(
                key, PYWALL_REG_FOLDER, 0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(PYWALL_FOLDER_KEY, 'Icon', 0,
                              winreg.REG_SZ, str(pyWallPath(folder)) + ",0")
            winreg.CloseKey(PYWALL_FOLDER_KEY)
        except Exception as e:
            print(f"Warning: Could not set folder icon: {e}")

        for x in sub_keys:
            current_sub_key = winreg.QueryValue(key, x)
            arg_index = winreg.QueryValue(key, x).index(" -c ")
            current_sub_key = current_sub_key.replace(
                r"([' '.join(sys.argv[1:]) ],'", ",").replace("')\"", ",")
            # About the dumbest way to query for the third semicolon #
            firstSemi = current_sub_key.find(";")
            secondSemi = current_sub_key.find(";", firstSemi + 1)
            thirdSemi = current_sub_key.find(";", secondSemi + 1)
            # The context menu must be tested with a compiled version of PyWall, otherwise it won't work #
            # PR's that address this are welcome #
            replacement_sub_key = current_sub_key[:arg_index +
                                                  4] + current_sub_key[thirdSemi + 1:]
            winreg.SetValue(key, x, winreg.REG_SZ, replacement_sub_key)

    except Exception as e:
        print(f"Error updating registry: {e}")


def removeInternetAccessMenu():
    menus.removeMenu('PyWall', type='FILES')
    menus.removeMenu("PyWall", type="DIRECTORY")
