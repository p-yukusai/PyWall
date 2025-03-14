"""
Notification and message display functionality for PyWall.
"""

import sys
import os
from PyQt5.QtWidgets import QMessageBox, QApplication, QStyle
from windows_toasts import ToastDuration

from src.config import get_config


def icons(icon_type="info"):
    """Get the appropriate icon for message boxes"""
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    style = app.style()

    icon_map = {
        "info": style.standardIcon(QStyle.SP_MessageBoxInformation),
        "warning": style.standardIcon(QStyle.SP_MessageBoxWarning),
        "critical": style.standardIcon(QStyle.SP_MessageBoxCritical),
        "question": style.standardIcon(QStyle.SP_MessageBoxQuestion)
    }

    return icon_map.get(icon_type.lower(), icon_map["info"])


def infoMessage(title, subtitle, message, icon=None):
    """Display an information message box"""
    if get_config("UI", "show_notifications") != "True":
        return

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    msg = QMessageBox()
    msg.setWindowTitle(title)
    if subtitle:
        msg.setText(subtitle)
    msg.setInformativeText(message)

    if icon:
        msg.setIcon(QMessageBox.Information)
        msg.setIconPixmap(icon.pixmap(32, 32))

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
        newToast = Toast()

        icon_path = None

        # Try to find the icon file
        script_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        possible_icon = os.path.join(script_dir, "resources", "PyWall.ico")
        if not(os.path.exists(possible_icon)):
            possible_icon = os.path.join(script_dir, "img", "PyWall.ico")
        if os.path.exists(possible_icon):
            icon_path = possible_icon

        newToast.text_fields = [title, message]
        print(newToast.text_fields)
        newToast.AddImage(ToastDisplayImage.fromPath(possible_icon))
        newToast.duration = ToastDuration.Default
        toaster.show_toast(newToast)

    except ImportError:
        # Fall back to message box if the current windows toast library is not available
        infoMessage(title, None, message)
