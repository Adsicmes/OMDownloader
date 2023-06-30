from PySide6.QtWidgets import QMessageBox


def error_message(title, text):
    """
    only use it when main window is now init or exit
    """
    msgBox = QMessageBox()
    msgBox.setWindowTitle(title)
    msgBox.setText(text)
    msgBox.exec_()
