from PyQt5.QtWidgets import QMessageBox
from winotify import Notification
from src.configGui import returnIcon


def toastNotification(title: str, msg: str):
    toast = Notification(app_id="PyWall", title=title, icon=str(returnIcon(True)).replace("ico", "png"), msg=msg)
    toast.build().show()


def infoMessage(text: str, title: str, information: str, icon: QMessageBox):
    from src.configGui import UI
    UI.messageBox(text, title, information, icon)


def icons(icon):
    if icon == "info" or "Info" or "INFO" or "information" or "Information" or "INFORMATION":  # Options! #
        return QMessageBox.Information
    elif icon == "critical" or "Critical" or "CRITICAL":
        return QMessageBox.Critical
    elif icon == "warning" or "Warning" or "WARNING":
        return QMessageBox.Warning
