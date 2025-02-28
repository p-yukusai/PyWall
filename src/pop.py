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
    if icon in ["info", "Info", "INFO", "information", "Information", "INFORMATION"]:
        return QMessageBox.Information
    elif icon in ["critical", "Critical", "CRITICAL"]:
        return QMessageBox.Critical
    elif icon in ["warning", "Warning", "WARNING"]:
        return QMessageBox.Warning
    else:
        return QMessageBox.NoIcon
