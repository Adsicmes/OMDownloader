import os

import i18n
from loguru import logger

from packages.common import DataFilePath
from packages.common import backgroundTaskQueue
from packages.common import loggedUser
from packages.common import osuWebApi
from packages.common import signalBus


def logout_exec():
    logger.info("Osu account is loging out...")
    quid = backgroundTaskQueue.createQueue()
    logoutThread = backgroundTaskQueue.createTaskWithNewThread(_logout)


def _logout():
    if loggedUser.isLogged:
        osuWebApi.logout()
        signalBus.usernameUpdate.emit(i18n.t("app.mainWindow.guest"))
        signalBus.avatarUpdate.emit(":/res/raw/images/osu-avatar-guest.png")

        loggedUser.isLogged = False

        if os.path.isfile(DataFilePath.userLoginInfo):
            logger.success("Remove user password file...")
            os.remove(DataFilePath.userLoginInfo)

        logger.success("Logout done.")
