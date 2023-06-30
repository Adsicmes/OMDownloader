import i18n
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentWindow
from qfluentwidgets.common.icon import FluentIcon as FIF
from qfluentwidgets.common.style_sheet import setTheme, Theme
from qfluentwidgets.components.navigation.navigation_interface import NavigationItemPosition

from packages.config import config
from .components import AvatarWidget
from .pages import *


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.mapDownloadInterface = MapDownloadInterface(self)
        self.initNavigation()

        self.initWindow()

    def initNavigation(self):
        # add navigation items
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Home'))
        self.navigationInterface.addSeparator()

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.mapDownloadInterface,
                             FIF.DOWNLOAD,
                             i18n.t("app.mainWindow.mapDownloadInterface"),
                             pos)

        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=AvatarWidget(self),
            onClick=lambda: ...,
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
        self.resize(1300, int(1300 * 9 / 16))
        self.setMinimumWidth(1300)
        self.setMinimumHeight(int(1300 * 9 / 16))
        self.setWindowIcon(QIcon(':res/raw/osu_icon.png'))
        self.setWindowTitle(i18n.t("app.mainWindow.appTitle"))
        self.setApplicationTheme()

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
