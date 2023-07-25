import i18n
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QFrame, QVBoxLayout
from qfluentwidgets import (ScrollArea, ProgressBar, PopUpAniStackedWidget, isDarkTheme,
                            PrimaryPushButton, FluentIcon)

from packages.common.task_queue import taskList
from packages.services.task.taskList import Task
from packages.view.common.stylesheet_manager import StyleSheet


class TaskCard(QWidget):
    def __init__(self, task: Task, parent=None):
        super().__init__(parent=parent)
        self.initWidget()
        self.initLayout()
        self.initInfo(task)

    def initWidget(self):
        self.setObjectName("TaskCard")

        self.nameLabel = QLabel(self)
        self.nameLabel.setObjectName("Name")
        self.nameLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)

        self.uuidLabel = QLabel(self)
        self.uuidLabel.setObjectName("UUID")
        self.uuidLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.uuidLabel.setContentsMargins(0, 0, 0, 3)

        self.startButton = PrimaryPushButton(self)
        self.startButton.setText(i18n.t("app.taskPage.buttonStatStart"))
        self.startButton.setIcon(FluentIcon.CARE_RIGHT_SOLID)
        self.startButton.clicked.connect(self.onStart)
        self.startButton.setFixedWidth(130)
        self.startButton.setContentsMargins(0, 5, 0, 0)

        self.msgLabel = QLabel(self)
        self.msgLabel.setObjectName("Msg")
        self.msgLabel.setContentsMargins(5, 0, 0, 5)
        self.msgLabel.setText(i18n.t("app.taskPage.msgLabel"))

        self.progressNum = QLabel(self)
        self.progressNum.setObjectName("ProgressNum")
        self.progressNum.setText("0%")
        self.progressNum.setFixedWidth(40)
        self.progressNum.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress = ProgressBar(self)
        self.progress.setObjectName("Progress")

        StyleSheet.TASK_INTERFACE.apply(self)

    def initLayout(self):
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(20, 10, 20, 20)
        self.vBoxLayout.setSpacing(24)

        self.infoLineLayout = QHBoxLayout()
        self.infoLineLayout.addWidget(self.nameLabel)
        self.infoLineLayout.addWidget(self.uuidLabel)
        self.infoLineLayout.addStretch()
        self.infoLineLayout.addWidget(self.startButton)

        self.progressLayout = QHBoxLayout()
        self.progressLayout.addWidget(self.progressNum)
        self.progressLayout.addWidget(self.progress)

        self.vBoxLayout.addLayout(self.infoLineLayout)
        self.vBoxLayout.addWidget(self.msgLabel)
        self.vBoxLayout.addLayout(self.progressLayout)

    def initInfo(self, task: Task):
        self.nameLabel.setText(task.name)
        self.uuidLabel.setText(task.uid)

        task.progressUpdate.connect(self.updateProgress)
        task.msgUpdate.connect(self.updateMsg)

    def updateMsg(self, text: str):
        self.msgLabel.setText(text)

    def updateProgress(self, progress: int):
        self.progress.setValue(progress)
        self.progressNum.setText(f"{progress}%")
        if progress >= 100:
            self.onDone()

    def onStart(self):
        self.startButton.setEnabled(False)
        taskList.start(self.uuidLabel.text())
        self.startButton.setText(i18n.t("app.taskPage.buttonStatProcessing"))

    def onDone(self):
        self.startButton.setEnabled(True)
        self.startButton.clicked.disconnect(self.onStart)
        self.startButton.setText(i18n.t("app.taskPage.buttonStatDone"))
        self.startButton.setIcon(FluentIcon.DELETE)
        self.startButton.clicked.connect(self.onDelete)

    def onDelete(self):
        taskList.remove(self.uuidLabel.text())

    def paintEvent(self, e) -> None:
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing)

        painter.setPen(Qt.NoPen)

        c = 255 if isDarkTheme() else 0
        painter.setBrush(QColor(c, c, c, 10))
        painter.drawRoundedRect(self.rect(), 10, 10)


class TaskArea(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.vBoxLayout = QVBoxLayout()
        self.setLayout(self.vBoxLayout)
        self.vBoxLayout.setContentsMargins(20, 10, 20, 10)
        self.vBoxLayout.setSpacing(24)

        taskList.taskStatUpdate.connect(self.updateAllTasks)

    def updateAllTasks(self):
        while self.vBoxLayout.count():
            child = self.vBoxLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for task in taskList.tasks:
            card = TaskCard(task, self)
            self.vBoxLayout.addWidget(card)

        self.vBoxLayout.addStretch()


class TaskScrollArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.taskArea = TaskArea(self)
        self.initLayout()

        StyleSheet.TASK_INTERFACE.apply(self)

    def initLayout(self):
        self.hBoxLayout = QHBoxLayout(self)
        self.scrollArea = ScrollArea(self)

        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.verticalScrollBar().setValue(0)
        self.scrollArea.setFrameShape(QFrame.NoFrame)  # noqa
        self.scrollArea.ensureWidgetVisible(self.taskArea)

        self.scrollArea.setWidget(self.taskArea)
        self.hBoxLayout.addWidget(self.scrollArea)


class NoTaskArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.initWidget()

    def initWidget(self):
        self.label = QLabel(i18n.t("app.taskPage.noTask"))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label)

        StyleSheet.TASK_INTERFACE.apply(self)


class TaskInterface(PopUpAniStackedWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("TaskInterface")

        self.noTaskArea = NoTaskArea(self)
        self.taskArea = TaskScrollArea(self)

        taskList.taskStatUpdate.connect(self.checkTasks)

        self.addWidget(self.noTaskArea)
        self.addWidget(self.taskArea)

        self.checkTasks()

        StyleSheet.TASK_INTERFACE.apply(self)

    def checkTasks(self):
        if not taskList.tasks:
            self.setCurrentWidget(self.noTaskArea)
        else:
            self.setCurrentWidget(self.taskArea)
