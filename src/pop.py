from PyQt5.QtWidgets import QMessageBox
from win10toast import ToastNotifier
from src.configGui import returnIcon


def toastNotification(title: str, msg: str, duration: int, threaded: bool):
    toast = ToastNotifier()
    toast.show_toast(title=title, icon_path=returnIcon(True), msg=msg, duration=duration, threaded=threaded)


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
