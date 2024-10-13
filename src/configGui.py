import pathlib
import sys
from sys import exception

import src.shellHandler
import PyQt5.QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from qt_material import apply_stylesheet, list_themes
from src.config import getConfig, config_read, modifyConfig, appendConfig, removeConfig, default
from src.logger import actionLogger

uiFile = 'src/ui/configGui.ui'
iconFile = 'img/PyWall.png'


# About the most roundabout way to write the folder where the exe/code is kept #

def getScriptFolder():
    from src.config import documentFolder
    document_folder = documentFolder()
    return document_folder + "\\PyWall\\Executable.txt"

try:
    with open(getScriptFolder(), 'r') as sf:
        folder = sf.read()
        if pathlib.Path(folder).exists():
            pass
        else:
            raise FileNotFoundError
except FileNotFoundError:
    from src.config import scriptFolder

    scriptFolder()
    with open(getScriptFolder(), 'r') as sf:
        folder = sf.read()

# I would bleach my eyes if I were you, that was awful #

uiFile_exception = folder + "//" + uiFile
iconFile_exception = folder + "//" + iconFile
stylesheet = getConfig("GUI", "stylesheet")
allThemes = list_themes()


def returnIcon(exception: bool):
    if exception:
        return pathlib.Path(iconFile_exception)
    else:
        return pathlib.Path(iconFile)


class UI(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        # Init and loading #
        try:
            super(UI, self).__init__()
            self.main = uic.loadUi(uiFile, self)
            self.setWindowIcon(QIcon(iconFile))
        except FileNotFoundError:
            super(UI, self).__init__()
            self.main = uic.loadUi(uiFile_exception, self)
            self.setWindowIcon(QIcon(iconFile_exception))
        # Defaults #
        with open(config_read(), "r") as cfg:
            self.configFileBrowser.setText(cfg.read())
        self.versionLabel.setText(f"Version: {getConfig('DEBUG', 'version')}")
        theme_string = []
        for x in allThemes:
            theme_string.append((x.replace(".xml", "").replace("_", " ")).title())
        self.themeComboBox.addItems(theme_string)
        current_theme = getConfig("GUI", "stylesheet")
        current_theme_index = allThemes.index(current_theme)
        current_string = theme_string[current_theme_index]
        self.themeComboBox.setCurrentText(current_string)
        if getConfig("FILETYPE", "recursive") == "True":
            self.recursiveCheckbox.setChecked(True)
        if getConfig("DEBUG", "create_logs") == "True":
            self.actionlogCheckbox.setChecked(True)
        if getConfig("DEBUG", "create_exception_logs") == "True":
            self.exceptionlogCheckbox.setChecked(True)
        # --- # Path # --- #
        self.fileSelect.clicked.connect(self.selectedFile)
        self.folderSelect.clicked.connect(self.selectedFolder)
        # --- # ComboBox # --- #
        self.recursiveCheckbox.stateChanged.connect(self.recursiveChanged)
        self.actionlogCheckbox.stateChanged.connect(self.actionlogChanged)
        self.exceptionlogCheckbox.stateChanged.connect(self.exceptionlogChanged)
        # --- # Access # --- #
        self.allowAccess.clicked.connect(lambda: self.internet_handler("allow"))
        self.denyAccess.clicked.connect(lambda: self.internet_handler("deny"))
        # --- # Rule Type # --- #
        self.outbound_check.setChecked(True)
        # --- # Config # --- #
        self.refreshButton.clicked.connect(self.refreshFile)
        self.saveButton.clicked.connect(self.saveFile)
        self.openConfigButton.clicked.connect(self.editThread)
        # --- # Theming # --- #
        self.selectTheme.clicked.connect(self.selectStylesheet)
        # --- # Blacklist # --- #
        self.addBlacklist.clicked.connect(self.addToBlacklist)
        self.removeBlacklist.clicked.connect(self.removeFromBlacklist)
        # --- # Types # --- #
        self.addTypes.clicked.connect(self.addToTypes)
        self.removeTypes.clicked.connect(self.removeFromTypes)
        # --- # Shell # --- #
        self.installShell.clicked.connect(self.installShellHandler)
        self.removeShell.clicked.connect(self.removeShellHandler)
        # --- # First run # --- #
        first_time = getConfig("GUI", "first_run")
        if first_time == "True":
            firstRun(self=UI)
            modifyConfig("GUI", "first_run", "False")
        # Show self #
        self.show()

    # Shell #
    @staticmethod
    def installShellHandler():
        from src.pop import infoMessage, icons
        if getConfig("DEBUG", "shell") == "True":
            icon = icons("warning")
            message = "It seems that you have already installed the shell handler, if you believe this is a mistake " \
                      'please press open the config file and edit the "shell" variable from "True" to "False" and try' \
                      ' again.'
            infoMessage("Already installed", "Shell handler has already been created", message, icon)
            return False
        src.shellHandler.createInternetAccessMenu()
        icon = icons("info")
        infoMessage("Shell handler successfully created.", "Successfully added", "You may now see the PyWall when right"
                                                                                 "-clicking a file or a folder.", icon)
        modifyConfig("DEBUG", "shell", "True")

    @staticmethod
    def removeShellHandler():
        from src.pop import infoMessage, icons
        if getConfig("DEBUG", "shell") == "False":
            icon = icons("warning")
            message = "The shell handler has either never been installed or has already been uninstalled, if you " \
                      'believe this to be a mistake, please open the config file and edit the "shell" variable from ' \
                      '"False" to "True" and try again.'
            infoMessage("Not installed", "Shell handler has not yet been installed", message, icon)
            return False
        src.shellHandler.removeInternetAccessMenu()
        icon = icons("info")
        infoMessage("Shell handler successfully removed.", "Successfully removed", "The PyWall option will no longer be"
                                                                                   " available when right-clicking a "
                                                                                   "file or a folder", icon)
        modifyConfig("DEBUG", "shell", "False")

    # Checkboxes #
    def recursiveChanged(self, state):
        if Qt.Checked == state:
            self.recursiveCheckbox.setChecked(True)
            modifyConfig("FILETYPE", "recursive", "True")
        else:

            self.recursiveCheckbox.setChecked(False)
            modifyConfig("FILETYPE", "recursive", "False")

    def actionlogChanged(self, state):
        if Qt.Checked == state:
            self.actionlogCheckbox.setChecked(True)
            modifyConfig("DEBUG", "create_logs", "True")
        else:
            self.actionlogCheckbox.setChecked(False)
            modifyConfig("DEBUG", "create_logs", "False")

    def exceptionlogChanged(self, state):
        if Qt.Checked == state:
            self.exceptionlogCheckbox.setChecked(True)
            modifyConfig("DEBUG", "create_exception_logs", "True")
        else:

            self.exceptionlogCheckbox.setChecked(False)
            modifyConfig("DEBUG", "create_exception_logs", "False")

    # Path handler #
    def selectedFile(self):
        path = PyQt5.QtWidgets.QFileDialog.getOpenFileName()[0]
        if pathlib.PureWindowsPath(path).suffix not in getConfig("FILETYPE", "accepted_types"):
            self.pathLineEdit.setText(f'Filetype "{pathlib.PureWindowsPath(path).suffix}"'
                                      f' in file "{pathlib.PureWindowsPath(path).name}" is not an accepted type.')
            actionLogger(f'Filetype not accepted, suffix for selected file'
                         f' is "{pathlib.PureWindowsPath(path).suffix}"')
            return
        actionLogger(f"Path for selected file is {path}")
        self.pathLineEdit.setText(path)

    def selectedFolder(self):
        path = PyQt5.QtWidgets.QFileDialog.getExistingDirectory()
        actionLogger(f"Path for selected folder is {path}")
        self.pathLineEdit.setText(path)

    # Internet access handler #
    def internet_handler(self, state):
        inbound = True if self.inbound_check.checkState() == 2 else False
        outbound = True if self.outbound_check.checkState() == 2 else False
        if not inbound and not outbound:
            self.pathLineEdit.setText("Please select one or more rule types before proceeding")
            return

        rule = "both" if inbound and outbound else "in" if inbound else "out"
        text = self.pathLineEdit.text()
        if text.startswith('"') and text.endswith('"'):
            text = text[1:text.__len__()-1]
        path = pathlib.Path(text)
        try:
            if text == "debug":
                pass
            elif text is None or not path.exists() or text == '':
                actionLogger("No valid path has been detected, aborting operation")
                return
        except OSError:
            actionLogger("Invalid, aborting operation")
            return

        if state == "allow":
            actionLogger(f"Attempting to allow internet access to {text}")
            from src.cmdWorker import access_handler
            access_handler(path, "allow", rule)
        elif state == "deny":
            actionLogger(f"Attempting to deny internet access to {text}")
            from src.cmdWorker import access_handler
            access_handler(path, "deny", rule)

    # GUI handlers #
    def saveFile(self):
        toWrite = str(self.configFileBrowser.toPlainText())
        with open(config_read(), "r") as cfg:
            current = cfg.read()
        if toWrite != current:
            with open(config_read(), "w") as cfg:
                cfg.write(toWrite)
            from src.pop import infoMessage, icons
            infoMessage("Success", "File successfully written", "Config.ini has been successfully updated",
                        icons("info"))
        else:
            actionLogger("No changes were made, skipping...")

    def refreshFile(self):
        with open(config_read(), "r") as cfg:
            self.configFileBrowser.setText(cfg.read())

    def selectStylesheet(self):
        themeIndex = self.themeComboBox.currentIndex()
        modifyConfig("GUI", "stylesheet", allThemes[themeIndex])
        apply_stylesheet(self.main, getConfig("GUI", "stylesheet"))

    def editThread(self):
        from threading import Thread
        editThread = Thread(target=self.openIni)
        editThread.start()

    @staticmethod
    def openIni():
        from src.cmdWorker import openConfig
        openConfig()

    # Blacklist handler #
    def addToBlacklist(self):
        ignoreFileName = self.blacklistLineEdit.text()
        if len(ignoreFileName) == 0:
            return False
        actionLogger("Adding to filename blacklist...")
        actionLogger(appendConfig("FILETYPE", "blacklisted_names", [ignoreFileName]))
        if ignoreFileName == "":
            return
        self.messageBox("Successfully added", "Success", f'Successfully added file "{ignoreFileName}" to the blacklist',
                        PyQt5.QtWidgets.QMessageBox.Information)

    def removeFromBlacklist(self):
        ignoreFileName = self.blacklistLineEdit.text()
        if len(ignoreFileName) == 0:
            return False
        actionLogger("Removing item from filename blacklist...")
        actionLogger(removeConfig("FILETYPE", "blacklisted_names", [ignoreFileName]))
        if ignoreFileName == "":
            return
        self.messageBox("Successfully removed", "Success", f'Successfully removed file "{ignoreFileName}" from'
                                                           f' the blacklist', PyQt5.QtWidgets.QMessageBox.Information)

    # Type handler #
    def addToTypes(self):
        typeSuffixName = self.typesLineEdit.text()
        try:
            if typeSuffixName[0] != ".":
                typeSuffixName = "." + typeSuffixName
        except IndexError:
            return False
        if typeSuffixName == ".":
            return False
        actionLogger("Adding suffix to accepted types...")
        actionLogger(appendConfig("FILETYPE", "accepted_types", [typeSuffixName]))
        if typeSuffixName == "." or "":
            return
        self.messageBox("Successfully added", "Success", f'Successfully added file "{typeSuffixName}" to accepted '
                                                         f'types', PyQt5.QtWidgets.QMessageBox.Information)

    def removeFromTypes(self):
        typeSuffixName = self.typesLineEdit.text()
        try:
            if typeSuffixName[0] != ".":
                typeSuffixName = "." + typeSuffixName
        except IndexError:
            return False
        if typeSuffixName == ".":
            return False
        actionLogger("Removing suffix from accepted types...")
        actionLogger(removeConfig("FILETYPE", "accepted_types", [typeSuffixName]))
        if typeSuffixName == "." or "":
            return
        self.messageBox("Successfully removed", "Success", f'Successfully removed file "{typeSuffixName}" from accepted'
                                                           f' types', PyQt5.QtWidgets.QMessageBox.Information)

    @staticmethod
    def messageBox(text: str, title: str, information=None, icon=PyQt5.QtWidgets.QMessageBox):
        msgBox = PyQt5.QtWidgets.QMessageBox()
        msgBox.setIcon(icon)
        msgBox.setText(text)
        msgBox.setWindowTitle(title)
        if information is not None:
            msgBox.setInformativeText(information)
        msgBox.setStandardButtons(PyQt5.QtWidgets.QMessageBox.Ok)
        try:
            msgBox.setWindowIcon(QIcon(iconFile))
        except FileNotFoundError:
            msgBox.setWindowIcon(QIcon(iconFile_exception))
        returnValue = msgBox.exec()

    def questionBoxHardCoded(self, text: str, title: str, information=None, icon=PyQt5.QtWidgets.QMessageBox):
        qBox = PyQt5.QtWidgets.QMessageBox()
        qBox.setIcon(icon)
        qBox.setText(text)
        qBox.setWindowTitle(title)
        if information is not None:
            qBox.setInformativeText(information)
        qBox.setStandardButtons(PyQt5.QtWidgets.QMessageBox.Yes | PyQt5.QtWidgets.QMessageBox.No)
        try:
            qBox.setWindowIcon(QIcon(iconFile))
        except FileNotFoundError:
            qBox.setWindowIcon(QIcon(iconFile_exception))
        returnValue = qBox.exec()
        if returnValue == PyQt5.QtWidgets.QMessageBox.Yes:
            self.installShellHandler()


def firstRun(self):
    self.questionBoxHardCoded(self, "Shell Handler installation prompt", "First run", "Hello! Thank you for installing"
                                                                                      " PyWall, would you like to "
                                                                                      "install a shell extension to "
                                                                                      "improve the utility of this "
                                                                                      "program? You can always install"
                                                                                      " or uninstall it later.",
                              PyQt5.QtWidgets.QMessageBox.Information)


# GUI Bootstrapper #
def start():
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    try:
        apply_stylesheet(app, theme=stylesheet)
    except ValueError:
        default()
        sheet = getConfig("GUI", "stylesheet")
        try:
            apply_stylesheet(app, theme=sheet)
        except ValueError:
            actionLogger("Unable to apply stylesheet, ignoring...")
            pass

    window = UI()
    app.exec_()
