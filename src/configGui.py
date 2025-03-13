import pathlib
import sys
import src.shellHandler
import PyQt5.QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5 import uic
from qt_material import apply_stylesheet, list_themes
from src.config import (
    get_config,
    config_file,
    modify_config,
    append_config,
    remove_config,
    default_config,
    document_folder,
    script_folder
)
from src.logger import actionLogger

uiFile = 'src/ui/configGui.ui'
iconFile = 'img/PyWall.png'


def getScriptFolder():
    """Get the folder where the executable/script information is stored"""
    document_folder_path = document_folder()
    return document_folder_path + "\\PyWall\\Executable.txt"


try:
    with open(getScriptFolder(), 'r') as sf:
        folder = sf.read()
        if pathlib.Path(folder).exists():
            pass
        else:
            raise FileNotFoundError
except FileNotFoundError:
    script_folder()
    with open(getScriptFolder(), 'r') as sf:
        folder = sf.read()


uiFile_exception = folder + "//" + uiFile
iconFile_exception = folder + "//" + iconFile
stylesheet = get_config("GUI", "stylesheet")
allThemes = list_themes()


def returnIcon(exception: bool):
    """Return the path to the icon file based on context"""
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

        # Initialize config tracking
        self.last_config_content = ""

        # Defaults #
        self.refreshFile()  # Use refreshFile instead of direct file read

        self.versionLabel.setText(f"Version: {get_config('DEBUG', 'version')}")

        # Theme handling with improved initialization
        theme_string = []
        for x in allThemes:
            theme_string.append(
                (x.replace(".xml", "").replace("_", " ")).title())

        self.themeComboBox.addItems(theme_string)
        try:
            current_theme = get_config("GUI", "stylesheet")
            if current_theme and current_theme in allThemes:
                current_theme_index = allThemes.index(current_theme)
                current_string = theme_string[current_theme_index]
                self.themeComboBox.setCurrentText(current_string)
                # Apply the saved theme
                apply_stylesheet(self.main, current_theme)
            else:
                # If no valid theme is saved, use default
                apply_stylesheet(self.main, "light_blue.xml")
                modify_config("GUI", "stylesheet", "light_blue.xml")
                self.themeComboBox.setCurrentText("Light Blue")
        except (ValueError, Exception) as e:
            actionLogger(f"Error initializing theme: {e}")
            self.themeComboBox.setCurrentText("Themes unavailable")

        # Set checkbox states from config
        self.updateUIFromConfig()

        # Connect signals to slots
        # Path buttons
        self.fileSelect.clicked.connect(self.selectedFile)
        self.folderSelect.clicked.connect(self.selectedFolder)

        # Checkboxes
        self.recursiveCheckbox.stateChanged.connect(self.recursiveChanged)
        self.actionlogCheckbox.stateChanged.connect(self.actionlogChanged)
        self.exceptionlogCheckbox.stateChanged.connect(
            self.exceptionlogChanged)

        # Access buttons
        self.allowAccess.clicked.connect(
            lambda: self.internet_handler("allow"))
        self.denyAccess.clicked.connect(lambda: self.internet_handler("deny"))

        # Rule type default
        self.outbound_check.setChecked(True)

        # Config buttons
        self.refreshButton.clicked.connect(self.refreshFile)
        self.saveButton.clicked.connect(self.saveFile)
        self.openConfigButton.clicked.connect(self.editThread)

        # Theme button
        self.selectTheme.clicked.connect(self.selectStylesheet)

        # Blacklist buttons
        self.addBlacklist.clicked.connect(self.addToBlacklist)
        self.removeBlacklist.clicked.connect(self.removeFromBlacklist)

        # Types buttons
        self.addTypes.clicked.connect(self.addToTypes)
        self.removeTypes.clicked.connect(self.removeFromTypes)

        # Shell buttons
        self.installShell.clicked.connect(self.installShellHandler)
        self.removeShell.clicked.connect(self.removeShellHandler)

        # First run check
        first_time = get_config("GUI", "first_run")
        if first_time == "True":
            firstRun(self=UI)
            modify_config("GUI", "first_run", "False")

        # Show self
        self.show()

    def updateCheckboxState(self, checkbox, state, section, key):
        """Update a checkbox state and corresponding config value"""
        if Qt.Checked == state:
            checkbox.setChecked(True)
            modify_config(section, key, "True")
        else:
            checkbox.setChecked(False)
            modify_config(section, key, "False")
        # Refresh config display after checkbox change
        self.refreshFile()

    def saveFile(self):
        """Save changes to the config file and refresh UI"""
        toWrite = str(self.configFileBrowser.toPlainText())
        try:
            with open(config_file(), "r") as cfg:
                current = cfg.read()

            if toWrite != current:
                with open(config_file(), "w") as cfg:
                    cfg.write(toWrite)
                from src.pop import infoMessage, icons
                infoMessage(
                    "Success",
                    "File successfully written",
                    "Config.ini has been successfully updated",
                    icons("info")
                )
                # Update last known content and refresh UI
                self.last_config_content = toWrite
                self.updateUIFromConfig()
                actionLogger("Config file saved successfully")
            else:
                actionLogger("No changes were made, skipping...")
        except Exception as e:
            actionLogger(f"Error saving config file: {e}")
            from src.pop import infoMessage, icons
            infoMessage(
                "Error",
                "Failed to save",
                f"Failed to save config file: {str(e)}",
                icons("error")
            )

    def refreshFile(self):
        """Refresh the config file display and update UI elements"""
        try:
            with open(config_file(), "r") as cfg:
                current_content = cfg.read()
                # Always update the text browser to show current content
                self.configFileBrowser.setText(current_content)
                # Only trigger UI updates if content has actually changed
                if current_content != self.last_config_content:
                    self.last_config_content = current_content
                    # Update UI elements based on current config
                    self.updateUIFromConfig()
                    actionLogger("Config file content changed, updating UI")
        except Exception as e:
            actionLogger(f"Error refreshing config file: {e}")

    def updateUIFromConfig(self):
        """Update all UI elements to match current config values"""
        # Update checkbox states
        self.recursiveCheckbox.setChecked(
            get_config("FILETYPE", "recursive") == "True")
        self.actionlogCheckbox.setChecked(
            get_config("DEBUG", "create_logs") == "True")
        self.exceptionlogCheckbox.setChecked(get_config(
            "DEBUG", "create_exception_logs") == "True")

        # Update theme selector
        try:
            current_theme = get_config("GUI", "stylesheet")
            if current_theme and current_theme in allThemes:
                theme_string = []
                for x in allThemes:
                    theme_string.append(
                        (x.replace(".xml", "").replace("_", " ")).title())
                current_theme_index = allThemes.index(current_theme)
                current_string = theme_string[current_theme_index]
                self.themeComboBox.setCurrentText(current_string)
                # Apply the saved theme
                apply_stylesheet(self.main, current_theme)
        except (ValueError, Exception) as e:
            actionLogger(f"Error updating theme from config: {e}")

    def selectStylesheet(self):
        """Apply the selected theme with proper validation and error handling"""
        themeIndex = self.themeComboBox.currentIndex()
        if themeIndex < 0 or themeIndex >= len(allThemes):
            actionLogger("Invalid theme index selected")
            return

        theme = allThemes[themeIndex]
        if not theme.endswith('.xml'):
            theme = theme + '.xml'

        # Verify theme exists
        if theme not in allThemes:
            actionLogger(f"Theme {theme} not found in available themes")
            return

        try:
            # Apply the theme
            apply_stylesheet(self.main, theme)

            # Update theme selector styling to match current theme
            self.themeComboBox.setStyleSheet("""
                QComboBox {
                    color: inherit;
                    background-color: transparent;
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox::down-arrow {
                    image: none;
                }
            """)

            # Save theme selection
            modify_config("GUI", "stylesheet", theme)
            actionLogger(f"Successfully applied theme: {theme}")
            # Refresh config display after theme change
            self.refreshFile()

        except Exception as e:
            actionLogger(f"Failed to apply theme: {e}")
            # Try to fallback to a safe theme
            try:
                apply_stylesheet(self.main, "light_blue.xml")
                modify_config("GUI", "stylesheet", "light_blue.xml")
                actionLogger("Falling back to light_blue theme")
                # Refresh config display after fallback
                self.refreshFile()
            except Exception as fallback_error:
                actionLogger(
                    f"Failed to apply fallback theme: {fallback_error}")

    def editThread(self):
        """Open the config file in a separate thread"""
        class ConfigEditorThread(QThread):
            finished = pyqtSignal()

            def run(self):
                from src.cmdWorker import open_config
                open_config()
                self.finished.emit()

        self.editor_thread = ConfigEditorThread()
        # Connect to both refreshFile and updateUIFromConfig to ensure complete update
        self.editor_thread.finished.connect(self.refreshFile)
        self.editor_thread.finished.connect(self.updateUIFromConfig)
        self.editor_thread.start()

    @staticmethod
    def openIni():
        """Open the config file in the default editor"""
        from src.cmdWorker import open_config
        open_config()

    # Blacklist handlers
    def addToBlacklist(self):
        """Add a filename to the blacklist"""
        ignoreFileName = self.blacklistLineEdit.text().strip()
        if not ignoreFileName:
            return False

        # Get current blacklist
        current_blacklist = get_config("FILETYPE", "blacklisted_names")
        if not current_blacklist:
            current_blacklist = ""
            items = []
        else:
            # Clean up any trailing commas
            current_blacklist = current_blacklist.rstrip(",")
            # Split by comma and clean up each item
            items = [item.strip()
                     for item in current_blacklist.split(",") if item.strip()]

        # Check if item already exists
        if ignoreFileName in items:
            self.messageBox(
                "Already exists",
                "Warning",
                f'File "{ignoreFileName}" is already in the blacklist',
                PyQt5.QtWidgets.QMessageBox.Warning
            )
            return False

        actionLogger("Adding to filename blacklist...")
        success = append_config(
            "FILETYPE", "blacklisted_names", [ignoreFileName])
        actionLogger(success)

        if success:
            self.messageBox(
                "Successfully added",
                "Success",
                f'Successfully added file "{ignoreFileName}" to the blacklist',
                PyQt5.QtWidgets.QMessageBox.Information
            )
            # Refresh config display after successful addition
            self.refreshFile()
        else:
            self.messageBox(
                "Addition failed",
                "Error",
                f'Failed to add file "{ignoreFileName}" to the blacklist',
                PyQt5.QtWidgets.QMessageBox.Critical
            )

    def removeFromBlacklist(self):
        """Remove a filename from the blacklist"""
        ignoreFileName = self.blacklistLineEdit.text().strip()
        if not ignoreFileName:
            return False

        actionLogger("Removing item from filename blacklist...")
        success = remove_config(
            "FILETYPE", "blacklisted_names", [ignoreFileName])
        actionLogger(success)

        if success:
            self.messageBox(
                "Successfully removed",
                "Success",
                f'Successfully removed file "{ignoreFileName}" from the blacklist',
                PyQt5.QtWidgets.QMessageBox.Information
            )
            # Refresh config display after successful removal
            self.refreshFile()
        else:
            self.messageBox(
                "Removal failed",
                "Error",
                f'Failed to remove file "{ignoreFileName}" from the blacklist',
                PyQt5.QtWidgets.QMessageBox.Critical
            )

    # File type handlers
    def addToTypes(self):
        """Add a file extension to the accepted types"""
        typeSuffixName = self.typesLineEdit.text().strip()
        if not typeSuffixName:
            return False

        if not typeSuffixName.startswith("."):
            typeSuffixName = "." + typeSuffixName

        if typeSuffixName == ".":
            return False

        # Get current accepted types
        current_types = get_config("FILETYPE", "accepted_types")
        if not current_types:
            current_types = ""
            items = []
        else:
            # Clean up any trailing commas
            current_types = current_types.rstrip(",")
            # Split by comma and clean up each item
            items = [item.strip()
                     for item in current_types.split(",") if item.strip()]

        # Check if type already exists
        if typeSuffixName in items:
            self.messageBox(
                "Already exists",
                "Warning",
                f'File type "{typeSuffixName}" is already in accepted types',
                PyQt5.QtWidgets.QMessageBox.Warning
            )
            return False

        actionLogger("Adding suffix to accepted types...")
        success = append_config("FILETYPE", "accepted_types", [typeSuffixName])
        actionLogger(success)

        if success:
            self.messageBox(
                "Successfully added",
                "Success",
                f'Successfully added file "{typeSuffixName}" to accepted types',
                PyQt5.QtWidgets.QMessageBox.Information
            )
            # Refresh config display after successful addition
            self.refreshFile()
        else:
            self.messageBox(
                "Addition failed",
                "Error",
                f'Failed to add file "{typeSuffixName}" to accepted types',
                PyQt5.QtWidgets.QMessageBox.Critical
            )

    def removeFromTypes(self):
        """Remove a file extension from the accepted types"""
        typeSuffixName = self.typesLineEdit.text().strip()
        if not typeSuffixName:
            return False

        if not typeSuffixName.startswith("."):
            typeSuffixName = "." + typeSuffixName

        if typeSuffixName == "." or typeSuffixName == "":
            return False

        actionLogger(
            f"Removing suffix '{typeSuffixName}' from accepted types...")
        success = remove_config("FILETYPE", "accepted_types", [typeSuffixName])
        actionLogger(success)

        if success:
            self.messageBox(
                "Successfully removed",
                "Success",
                f'Successfully removed file "{typeSuffixName}" from accepted types',
                PyQt5.QtWidgets.QMessageBox.Information
            )
            # Refresh config display after successful removal
            self.refreshFile()
        else:
            self.messageBox(
                "Removal failed",
                "Error",
                f'Failed to remove file "{typeSuffixName}" from accepted types',
                PyQt5.QtWidgets.QMessageBox.Critical
            )

    @staticmethod
    def messageBox(text: str, title: str, information=None, icon=PyQt5.QtWidgets.QMessageBox):
        """Display a message box"""
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
        """Display a question box with Yes/No options"""
        qBox = PyQt5.QtWidgets.QMessageBox()
        qBox.setIcon(icon)
        qBox.setText(text)
        qBox.setWindowTitle(title)
        if information is not None:
            qBox.setInformativeText(information)
        qBox.setStandardButtons(
            PyQt5.QtWidgets.QMessageBox.Yes | PyQt5.QtWidgets.QMessageBox.No)
        try:
            qBox.setWindowIcon(QIcon(iconFile))
        except FileNotFoundError:
            qBox.setWindowIcon(QIcon(iconFile_exception))
        returnValue = qBox.exec()
        if returnValue == PyQt5.QtWidgets.QMessageBox.Yes:
            self.installShellHandler()

    def checkConfigChanges(self):
        """Check if the config file has changed and update UI if needed"""
        try:
            with open(config_file(), "r") as cfg:
                current_content = cfg.read()
                if current_content != self.last_config_content:
                    self.last_config_content = current_content
                    self.refreshFile()
        except Exception as e:
            actionLogger(f"Error checking config changes: {e}")

    def selectedFile(self):
        """Handle file selection via dialog"""
        path = PyQt5.QtWidgets.QFileDialog.getOpenFileName()[0]
        if not path:
            return

        if pathlib.PureWindowsPath(path).suffix not in get_config("FILETYPE", "accepted_types"):
            self.pathLineEdit.setText(
                f'Filetype "{pathlib.PureWindowsPath(path).suffix}" '
                f'in file "{pathlib.PureWindowsPath(path).name}" is not an accepted type.'
            )
            actionLogger(
                f'Filetype not accepted, suffix for selected file '
                f'is "{pathlib.PureWindowsPath(path).suffix}"'
            )
            return

        actionLogger(f"Path for selected file is {path}")
        self.pathLineEdit.setText(path)

    def selectedFolder(self):
        """Handle folder selection via dialog"""
        path = PyQt5.QtWidgets.QFileDialog.getExistingDirectory()
        if not path:
            return

        actionLogger(f"Path for selected folder is {path}")
        self.pathLineEdit.setText(path)

    def internet_handler(self, state):
        """Handle allowing or denying internet access"""
        inbound = True if self.inbound_check.checkState() == 2 else False
        outbound = True if self.outbound_check.checkState() == 2 else False

        if not inbound and not outbound:
            self.pathLineEdit.setText(
                "Please select one or more rule types before proceeding")
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
                actionLogger(
                    "No valid path has been detected, aborting operation")
                return
        except OSError:
            actionLogger("Invalid, aborting operation")
            return

        if state == "allow":
            actionLogger(f"Attempting to allow internet access to {text}")
            from src.cmdWorker import access_handler
            access_handler(path, "allow", rule)
            # Refresh config display after access change
            self.refreshFile()
        elif state == "deny":
            actionLogger(f"Attempting to deny internet access to {text}")
            from src.cmdWorker import access_handler
            access_handler(path, "deny", rule)
            # Refresh config display after access change
            self.refreshFile()

    def recursiveChanged(self, state):
        self.updateCheckboxState(
            self.recursiveCheckbox, state, "FILETYPE", "recursive")

    def actionlogChanged(self, state):
        self.updateCheckboxState(
            self.actionlogCheckbox, state, "DEBUG", "create_logs")

    def exceptionlogChanged(self, state):
        self.updateCheckboxState(
            self.exceptionlogCheckbox, state, "DEBUG", "create_exception_logs")

    @staticmethod
    def installShellHandler():
        """Install the shell context menu handler"""
        from src.pop import infoMessage, icons
        if get_config("DEBUG", "shell") == "True":
            icon = icons("warning")
            message = ("It seems that you have already installed the shell handler, if you believe this is a mistake "
                       'please press open the config file and edit the "shell" variable from "True" to "False" and try'
                       ' again.')
            infoMessage("Already installed",
                        "Shell handler has already been created", message, icon)
            return False

        src.shellHandler.createInternetAccessMenu()
        icon = icons("info")
        infoMessage("Shell handler successfully created.", "Successfully added",
                    "You may now see the PyWall when right-clicking a file or a folder.", icon)
        modify_config("DEBUG", "shell", "True")

    @staticmethod
    def removeShellHandler():
        """Remove the shell context menu handler"""
        from src.pop import infoMessage, icons
        if get_config("DEBUG", "shell") == "False":
            icon = icons("warning")
            message = ("The shell handler has either never been installed or has already been uninstalled, if you "
                       'believe this to be a mistake, please open the config file and edit the "shell" variable from '
                       '"False" to "True" and try again.')
            infoMessage(
                "Not installed", "Shell handler has not yet been installed", message, icon)
            return False

        src.shellHandler.removeInternetAccessMenu()
        icon = icons("info")
        infoMessage("Shell handler successfully removed.", "Successfully removed",
                    "The PyWall option will no longer be available when right-clicking a file or a folder", icon)
        modify_config("DEBUG", "shell", "False")


def firstRun(self):
    """Handle first run actions"""
    self.questionBoxHardCoded(self, "Shell Handler installation prompt", "First run", "Hello! Thank you for installing"
                                                                                      " PyWall, would you like to "
                                                                                      "install a shell extension to "
                                                                                      "improve the utility of this "
                                                                                      "program? You can always install"
                                                                                      " or uninstall it later.",
                              PyQt5.QtWidgets.QMessageBox.Information)


# GUI Bootstrapper #
def start(bypass_stylesheet=False):
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    if not bypass_stylesheet:
        try:
            # Only apply default theme if no theme is set
            current_theme = get_config("GUI", "stylesheet")
            if not current_theme or current_theme == "":
                apply_stylesheet(app, theme="dark_red.xml")
                modify_config("GUI", "stylesheet", "dark_red.xml")
            else:
                apply_stylesheet(app, theme=current_theme)
        except ValueError:
            actionLogger("Unable to apply stylesheet")
            pass

    window = UI()
    window.show()
    return app.exec_()
