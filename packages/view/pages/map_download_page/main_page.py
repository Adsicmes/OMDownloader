# coding:utf-8

import i18n
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel
from qfluentwidgets import SegmentedWidget

from packages.view.common.stylesheet_manager import StyleSheet
from .batch_download_page import BatchDownloadSubInterface


class MapDownloadInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("MapDownloadInterface")

        self.setContentsMargins(15, 15, 10, 10)

        self.pivot = SegmentedWidget(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.batchDownloadSubInterface = BatchDownloadSubInterface(self)
        self.albumInterface = QLabel('Album Interface', self)

        # add items to pivot
        self.addSubInterface(self.batchDownloadSubInterface, 'batchDownloadSubInterface',
                             i18n.t("app.mapDownloadPage.mainPage.batchDownload"))
        self.addSubInterface(self.albumInterface, 'albumInterface', 'Album')

        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(0, 0, 30, 30)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.batchDownloadSubInterface)
        self.pivot.setCurrentItem(self.batchDownloadSubInterface.objectName())

        StyleSheet.MAP_DOWNLOAD_INTERFACE.apply(self)

    def addSubInterface(self, widget: QWidget, objectName, text):
        widget.setObjectName(objectName)
        # widget.setAlignment(Qt.AlignCenter)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())
