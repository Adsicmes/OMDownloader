from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, QBrush
from PySide6.QtWidgets import QWidget

from packages.view.common.stylesheet_manager import StyleSheet


class HomeInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("HomeInterface")

        self.bg = QPixmap(":/res/raw/images/000_homepage_bg.png")

        StyleSheet.HOME_INTERFACE.apply(self)

    def paintEvent(self, e):
        """
        background drawer
        """
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        w, h = self.width(), self.height()
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        # path.addRect(QRectF(0, h - 50, 50, 50))
        # path.addRect(QRectF(w - 50, 0, 50, 50))
        # path.addRect(QRectF(w - 50, h - 50, 50, 50))
        path = path.simplified()

        # # draw background color
        # if not isDarkTheme():
        #     painter.fillPath(path, QColor(206, 216, 228))
        # else:
        #     painter.fillPath(path, QColor(0, 0, 0))

        # draw banner image
        pixmap = self.bg.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        path.addRect(QRectF(0, h, w, self.height() - h))
        painter.fillPath(path, QBrush(pixmap))
