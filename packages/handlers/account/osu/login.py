import os
import pickle

import httpx

from packages.common import DataFilePath
from packages.common import loggedUser
from packages.common import osuWebApi
from packages.common import signalBus
from packages.common import taskQueue
from packages.config import config
from packages.model.osu_web.user import UserModel
from packages.utils import getNowUnixTimestamp


def login_exec(username, password):
    quid = taskQueue.createQueue()
    loginThread = taskQueue.createTaskWithNewThread(_login, 0, username, password, quid)
    handleThread = taskQueue.createTaskWithNewThread(_loginHandle, 0, username, password, quid)


def _login(username, password, quid):
    q = taskQueue.findQueue(quid)
    q.put(osuWebApi.login(username, password).json())


def _loginHandle(username, password, quid):
    q = taskQueue.findQueue(quid)
    info = q.get()["user"]

    # change loggedUser status
    loggedUser.isLogged = True
    loggedUser.userInfo = UserModel(**info)
    loggedUser.lastUpdate = getNowUnixTimestamp()

    # change avatar and username in interface
    signalBus.usernameUpdate.emit(info["username"])
    avatarDownloadThread = taskQueue.createTaskWithNewThread(_avatarDownload, 0, info["avatar_url"])

    # pickle username and password to local data
    pickle.dump((username, password), open(DataFilePath.userLoginInfo, "wb"))


def _avatarDownload(url):
    fp = os.path.join(config["others"]["cacheLocation"], f"avatar.{url.split('.')[-1]}")
    with open(fp, "wb") as f:
        f.write(httpx.get(url).content)
    signalBus.avatarUpdate.emit(fp)
