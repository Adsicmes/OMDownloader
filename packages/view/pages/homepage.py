from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel

from ..common.stylesheet_manager import StyleSheet


class HomeInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("HomeInterface")

        font = QFont()
        font.setFamily("Segoe Fluent Icons")
        self.testLabel = QLabel()
        self.testLabel.setFont(font)
        self.testLabel.setText("dwdw")
        self.testLabel.setParent(self)

        self.testLabel.move(130, 150)

        StyleSheet.HOME_INTERFACE.apply(self)
