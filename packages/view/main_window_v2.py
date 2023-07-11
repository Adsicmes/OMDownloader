import i18n
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentWindow  # , SplashScreen
from qfluentwidgets.common.icon import FluentIcon as FIF
from qfluentwidgets.common.style_sheet import setTheme, Theme
from qfluentwidgets.components.navigation.navigation_interface import NavigationItemPosition
from qframelesswindow import TitleBar

from packages.config import config
from .components import (AvatarWidget,
                         SplashScreenWithFadeOut as SplashScreen,
                         FluentTitleBarWithVersionNumber as TitleBar)
from .pages import *


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.mapDownloadInterface = MapDownloadInterface(self)
        self.avatar = AvatarWidget(self)

        self.initNavigation()
        self.splashScreen.finish()

    def initNavigation(self):
        # add navigation items
        self.addSubInterface(self.homeInterface, FIF.HOME, i18n.t("app.mainWindow.homeInterface"))
        self.navigationInterface.addSeparator()

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.mapDownloadInterface,
                             FIF.DOWNLOAD,
                             i18n.t("app.mainWindow.mapDownloadInterface"),
                             pos)

        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=self.avatar,
            onClick=lambda: self.avatar.onClicked(self.avatar, self),
            position=NavigationItemPosition.BOTTOM
        )

    @staticmethod
    def setApplicationTheme():
        cfg_theme = config["view"]["theme"]
        if cfg_theme == "dark":
            setTheme(Theme.DARK)
        elif cfg_theme == "light":
            setTheme(Theme.LIGHT)
        else:
            setTheme(Theme.AUTO)

    def initWindow(self):
        self.setTitleBar(TitleBar(self))
        self.resize(1300, int(1300 * 9 / 16))
        self.setMinimumWidth(1300)
        self.setMinimumHeight(int(1300 * 9 / 16))
        self.setWindowIcon(QIcon(':res/raw/osu_icon.png'))
        self.setWindowTitle(i18n.t("app.mainWindow.appTitle"))

        self.setApplicationTheme()

        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()
