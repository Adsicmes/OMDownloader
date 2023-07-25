import os

import i18n

from packages.common import DataFilePath
from packages.common import backgroundTaskQueue
from packages.common import loggedUser
from packages.common import osuWebApi
from packages.common import signalBus


def logout_exec():
    quid = backgroundTaskQueue.createQueue()
    logoutThread = backgroundTaskQueue.createTaskWithNewThread(_logout)


def _logout():
    if loggedUser.isLogged:
        osuWebApi.logout()
        signalBus.usernameUpdate.emit(i18n.t("app.mainWindow.guest"))
        signalBus.avatarUpdate.emit(":/res/raw/images/osu-avatar-guest.png")

        loggedUser.isLogged = False

        if os.path.isfile(DataFilePath.userLoginInfo):
            os.remove(DataFilePath.userLoginInfo)
