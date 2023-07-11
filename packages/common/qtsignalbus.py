from PySide6.QtCore import Signal, QObject


class QtSignalBus(QObject):
    avatarUpdate = Signal(str)
    usernameUpdate = Signal(str)


signalBus = QtSignalBus()
