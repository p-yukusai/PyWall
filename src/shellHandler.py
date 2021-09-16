import os
import pathlib
from context_menu import menus


# Having to define stuff anew in this script, since it's technically separate in the context of the shell #
def documentFolder():
    import ctypes.wintypes
    doc = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, doc)
    document_folder = doc.value
    return document_folder


def getScriptFolder():
    document_folder = documentFolder()
    return document_folder + "\\PyWall\\Executable.txt"
# Making the messagebox in Qt saves space in the executable, otherwise we would have the good old Tkinter bloat #
def pop(title, text, close: bool):
    import sys
    from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

    def window():
        app = QApplication(sys.argv)
        win = QWidget()
        showDialog()
        sys.exit(app.exec_())

    def showDialog():
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        if close:
            sys.exit(0)

    window()


# The "open" command is repeated because I'm too lazy to define it and then just call it later, code redundancy go brr #
def allowAccess(filenames, params):
    try:
        with open(getScriptFolder(), 'r') as sf:
            folder = sf.read()
    except FileNotFoundError:
        pop("PyWall.exe not found", "Could not find PyWall, please open the program and try again.", True)

    try:
        if pathlib.Path(folder + "//PyWall.exe").is_file() or pathlib.Path(folder + "//main.py").is_file():
            os.system(f'cmd /c cd {folder} && PyWall.exe -file {filenames} -allow true')
            # input() #
            os.system(f'cmd /c cd {folder} && python {folder}\main.py -file {filenames} -allow true')
            # input() #
        else:
            os.remove(getScriptFolder())
            pop("PyWall.exe not found", "Could not find PyWall, please open the program and try again.", True)
    except FileNotFoundError:
        pop("PyWall.exe not found", "Could not find PyWall, please open the program and try again.", True)


def denyAccess(filenames, params):
    try:
        with open(getScriptFolder(), 'r') as sf:
            folder = sf.read()
    except FileNotFoundError:
        pop("PyWall.exe not found", "Could not find PyWall, please open the program and try again.", True)

    try:
        if pathlib.Path(folder + "//PyWall.exe").is_file() or pathlib.Path(folder + "//main.py").is_file():
            os.system(f'cmd /c cd {folder} && PyWall.exe -file {filenames}')
            # input() #
            os.system(f'cmd /c cd {folder} && python {folder}\main.py -file {filenames} ')
            # input() #
        else:
            os.remove(getScriptFolder())
            pop("PyWall.exe not found", "Could not find PyWall, please open the program and try again.", True)
    except FileNotFoundError:
        pop("PyWall.exe not found", "Could not find PyWall, please open the program and try again.", True)


# This creates the context menu, It is important to do this for FILES and for DIRECTORY so that the user can right #
# click on either. The keys created are in "HKEY_CURRENT_USER\Software\Classes\*\shell\" for FILES and in #
# "HKEY_CURRENT_USER\Software\Classes\Directory\shell" for DIRECTORY #
def createInternetAccessMenu():
    IAM = menus.ContextMenu('PyWall', type='FILES')
    IAM.add_items([menus.ContextCommand('Allow Internet Access', python=allowAccess),
                   menus.ContextCommand('Deny Internet Access', python=denyAccess)])
    IAM.compile()

    IAM_Folder = menus.ContextMenu('PyWall', type='DIRECTORY')
    IAM_Folder.add_items([menus.ContextCommand('Allow Internet Access', python=allowAccess),
                          menus.ContextCommand('Deny Internet Access', python=denyAccess)])
    IAM_Folder.compile()

    # This is a to bypass a limitation of context_menu, or rather, of the "Run" command. #
    # In brief, the run command can only be a certain length, so we're removing some of the text from the handler #
    # and replacing it with a custom parser in "main.py" #
    import winreg

    IAM_FILES_ALLOW = r"Software\Classes\*\shell\PyWall\shell\Allow Internet Access\command"
    IAM_FILES_DENY = r"Software\Classes\*\shell\PyWall\shell\Deny Internet Access\command"
    IAM_DIR_ALLOW = r"Software\Classes\Directory\shell\PyWall\shell\Allow Internet Access\command"
    IAM_DIR_DENY = r"Software\Classes\Directory\shell\PyWall\shell\Deny Internet Access\command"
    key = winreg.HKEY_CURRENT_USER
    sub_keys = [IAM_FILES_ALLOW, IAM_FILES_DENY, IAM_DIR_ALLOW, IAM_DIR_DENY]

    for x in sub_keys:
        current_sub_key = winreg.QueryValue(key, x)
        argIndex = winreg.QueryValue(key, x).index(" -c ")
        # About the dumbest way to query for the third semi-colon #
        firstSemi = current_sub_key.find(";")
        secondSemi = current_sub_key.find(";", firstSemi + 1)
        thirdSemi = current_sub_key.find(";", secondSemi + 1)
        if "shellHandler.allowAccess" in current_sub_key:
            accessIndex = current_sub_key.find("shellHandler.allowAccess") + 24
        else:
            accessIndex = current_sub_key.find("shellHandler.denyAccess") + 23
        quoteIndex = current_sub_key.find('"', thirdSemi)
        replacement_sub_key = current_sub_key[:argIndex + 4] + current_sub_key[thirdSemi + 1: accessIndex] + \
                              current_sub_key[quoteIndex:]
        winreg.SetValue(key, x, winreg.REG_SZ, replacement_sub_key)


def removeInternetAccessMenu():
    menus.removeMenu('PyWall', type='FILES')
    menus.removeMenu("PyWall", type="DIRECTORY")
