# coding: utf-8
from typing import Union

import i18n
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QImage, QBrush, QColor, QFont
from PySide6.QtWidgets import QApplication, QVBoxLayout, QLineEdit
from qfluentwidgets import NavigationWidget, isDarkTheme, FlyoutViewBase, BodyLabel, PopupTeachingTip, \
    TeachingTipTailPosition, PrimaryPushButton, LineEdit

from packages.common import signalBus
from packages.handlers.account.osu.login import login_exec


# class CustomFlyoutView(FlyoutViewBase):
#
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.hBoxLayout = QHBoxLayout()
#         self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
#
#         self.loginLabel = QLabel(i18n.t("app.mainWindow.avatar.loginLabel"), self)
#         self.hBoxLayout.addWidget(self.loginLabel)
#
#     def paintEvent(self, e):
#         pass


class CustomFlyoutView(FlyoutViewBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.label = BodyLabel('Login')
        self.label.setFont(QFont(QApplication.font().family(), 16))

        self.usernameLineEdit = LineEdit(self)
        self.usernameLineEdit.setPlaceholderText("Username")
        self.passwordLineEdit = LineEdit(self)
        self.passwordLineEdit.setPlaceholderText("Password")
        self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        self.button = PrimaryPushButton('Login')
        self.button.setFixedWidth(140)
        self.button.clicked.connect(self.on_login_clicked)

        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.setContentsMargins(20, 16, 20, 16)
        self.vBoxLayout.addWidget(self.label)
        self.vBoxLayout.addWidget(self.usernameLineEdit)
        self.vBoxLayout.addWidget(self.passwordLineEdit)
        self.vBoxLayout.addWidget(self.button, 0, Qt.AlignRight)

        self.setMinimumWidth(380)
        self.setContentsMargins(5, 10, 5, 10)

    def paintEvent(self, e):
        pass

    def on_login_clicked(self):
        try:
            if self.button.isEnabled():
                self.button.setEnabled(False)
            login_exec(self.usernameLineEdit.text(), self.passwordLineEdit.text())
        except Exception:
            self.button.setEnabled(True)


class AvatarWidget(NavigationWidget):
    """ Avatar widget """

    def __init__(self, parent=None):
        super().__init__(isSelectable=False, parent=parent)
        self.avatar = QImage(":/res/raw/images/osu-avatar-guest.png").scaled(
            24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.text = i18n.t("app.mainWindow.guest")
        self.textFont = QFont(QApplication.font().family(), 12)

        signalBus.usernameUpdate.connect(self.setText)
        signalBus.avatarUpdate.connect(self.setAvatarImage)

    def setText(self, text: str) -> None:
        self.text = text

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

    @staticmethod
    def onClicked(target, parent) -> None:
        PopupTeachingTip.make(
            target=target,
            view=CustomFlyoutView(),
            tailPosition=TeachingTipTailPosition.LEFT_BOTTOM,
            duration=-1,
            parent=parent
        )
