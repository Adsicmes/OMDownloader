from PySide6.QtCore import QObject

from packages.common.logged_user import loggedUser
from packages.common.qtsignalbus import signalBus
from packages.common.request import osuWebApi
from packages.services.request.normal import avatarDownload


class InfoUpdate(QObject):
    def __init__(self):
        super().__init__()
        signalBus.avatarUpdate.connect(self.avatarUpdate)

    @staticmethod
    def loginUserInfoUpdate():
        userId = loggedUser.userInfo["id"]
        newInfo, _ = osuWebApi.getUser(userId)
        loggedUser.updateUserInfo(newInfo)

    @staticmethod
    def avatarUpdate(url: str):
        if url.startswith("http"):
            avatarDownload(url)
            signalBus.avatarUpdate.emit(url)

    @staticmethod
    def coverUpdate(url: str):
        if url.startswith("http"):
            avatarDownload(url)
            signalBus.coverUpdate.emit(url)


infoUpdate = InfoUpdate()
