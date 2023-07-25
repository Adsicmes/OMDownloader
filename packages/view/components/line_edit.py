from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QFileDialog
from qfluentwidgets import FluentIcon
from qfluentwidgets import LineEdit, LineEditButton


class FolderSelectLineEdit(LineEdit):
    folderSignal = Signal(str)
    clearSignal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.folderButton = LineEditButton(FluentIcon.FOLDER, self)

        self.hBoxLayout.addWidget(self.folderButton, 0, Qt.AlignRight)
        self.setFolderButtonEnabled(True)
        self.setTextMargins(0, 0, 59, 0)

        self.folderButton.clicked.connect(self.search)
        self.clearButton.clicked.connect(self.clearSignal)

    def search(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        if dialog.exec_():
            selected_folders = dialog.selectedFiles()
            if selected_folders:
                selected_folder = selected_folders[0]
                self.setText(selected_folder)

    def setFolderButtonEnabled(self, enable: bool):
        self._isClearButtonEnabled = enable
        self.setTextMargins(0, 0, 28 * enable + 30, 0)
