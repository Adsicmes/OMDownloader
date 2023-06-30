# coding: utf-8
from typing import Union

import i18n
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QImage, QBrush, QColor, QFont
from PySide6.QtWidgets import QApplication
from qfluentwidgets import NavigationWidget, isDarkTheme


class AvatarWidget(NavigationWidget):
    """ Avatar widget """

    def __init__(self, parent=None):
        super().__init__(isSelectable=False, parent=parent)
        self.avatar = QImage(":/res/raw/images/osu-avatar-guest.png").scaled(
            24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.text = i18n.t("app.mainWindow.guest")
        self.textFont = QFont(QApplication.font().family(), 12)

    def paintEvent(self, e) -> None:
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing)

        painter.setPen(Qt.NoPen)

        if self.isPressed:
            painter.setOpacity(0.7)

        # draw background
        if self.isEnter:
            c = 255 if isDarkTheme() else 0
            painter.setBrush(QColor(c, c, c, 10))
            painter.drawRoundedRect(self.rect(), 5, 5)

        # draw avatar
        painter.setBrush(QBrush(self.avatar))
        painter.translate(8, 6)
        painter.drawEllipse(0, 0, 24, 24)
        painter.translate(-8, -6)

        if not self.isCompacted:
            painter.setPen(Qt.white if isDarkTheme() else Qt.black)
            painter.setFont(self.textFont)
            painter.drawText(QRect(44, -2, 255, 36), Qt.AlignVCenter, self.text)

    def repaint(self) -> None:
        super().repaint()

    def setAvatarImage(self, image: Union[str, QImage]) -> None:
        if isinstance(image, str):
            image = QImage(image)
        elif isinstance(image, QImage):
            pass

        self.avatar = image.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.repaint()

    def setTextFont(self, font: Union[str, QFont]) -> None:
        if isinstance(font, str):
            font = QFont(font, self.textFont.pixelSize())
        elif isinstance(font, QFont):
            font.setPixelSize(self.textFont.pixelSize())

        self.textFont = font

    def setTextSize(self, size: int) -> None:
        self.textFont.setPixelSize(size)
