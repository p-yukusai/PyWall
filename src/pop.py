"""
Notification and message display functionality for PyWall.
"""

import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QApplication
from windows_toasts import ToastDuration

from src.config import get_config
from src.logger import actionLogger

# Try to find the icon file
script_dir = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))
possible_icon = os.path.join(script_dir, "resources", "PyWall.ico")
if not(os.path.exists(possible_icon)):
    possible_icon = os.path.join(script_dir, "img", "PyWall.ico")
if os.path.exists(possible_icon):
    icon_path = possible_icon

def icons(icon_type="info"):
    """Get the appropriate icon for message boxes"""
    icon_type.lower()
    if icon_type == "info":
        return QMessageBox.Information
    elif icon_type == "warning":
        return QMessageBox.Warning
    elif icon_type == "error":
        return QMessageBox.Critical
    elif icon_type == "question":
        return QMessageBox.Question
    elif icon_type == "pywall":
        pywall = QIcon(icon_path)
        return pywall
    else:
        return QMessageBox.Information


def infoMessage(title, subtitle, message, icon=None):
    """Display an information message box"""
    if get_config("UI", "show_notifications") != "True":
        return

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(message)
    if subtitle:
        msg.setInformativeText(subtitle)

    if icon:
        if type(icon) == str:
            msg.setIcon(icons(icon))
        else:
            msg.setIcon(icon)
        msg.setWindowIcon(icons("pywall"))
    msg.exec_()


def confirmDialog(title, message, icon=None):
    """Display a confirmation dialog and return True if user confirms"""
    if get_config("UI", "confirmation_dialog") != "True":
        return True

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msg.setDefaultButton(QMessageBox.No)

    if icon:
        msg.setIconPixmap(icon.pixmap(32, 32))
    else:
        msg.setIcon(QMessageBox.Question)

    return msg.exec_() == QMessageBox.Yes


def toastNotification(title, message):
    """Display a toast notification"""
    if get_config("UI", "show_notifications") != "True":
        return
    try:
        from windows_toasts import WindowsToaster, Toast, ToastDisplayImage
        toaster = WindowsToaster('PyWall')
        new_toast = Toast()
        new_toast.text_fields = [title, message]
        print(new_toast.text_fields)
        new_toast.AddImage(ToastDisplayImage.fromPath(possible_icon))
        new_toast.duration = ToastDuration.Default
        toaster.show_toast(new_toast)
    except ImportError as e:
        actionLogger(e)
        # Fall back to message box if the current windows toast library is not available
        actionLogger("Unable to import windows_toasts, using fallback")
        infoMessage(title, None, message, icons("warning"))