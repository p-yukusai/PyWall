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


def removeInternetAccessMenu():
    menus.removeMenu('PyWall', type='FILES')
    menus.removeMenu("PyWall", type="DIRECTORY")
