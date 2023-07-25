import pickle

import httpx

from packages.common import DataFilePath
from packages.common import backgroundTaskQueue
from packages.common import loggedUser
from packages.common import osuWebApi
from packages.common import retry
from packages.common import signalBus
from packages.config import config
from packages.model.osu_web.user import LoginUserModel
from packages.services.request.normal import avatarDownload
from packages.utils import getNowUnixTimestamp


def login_exec(username, password, isRemember):
    quid = backgroundTaskQueue.createQueue()
    loginThread = backgroundTaskQueue.createTaskWithNewThread(_login, 0, username, password, quid, isRemember)


@retry(delays=(1 for _ in range(int(config["Retry.ppy_sh"]))), exceptions=(httpx.HTTPError,))
def _login(username, password, quid, isRemember):
    q = backgroundTaskQueue.findQueue(quid)
    while q.qsize() != 0:
        q.get()

    q.put(info := osuWebApi.login(username, password).json())
    q.put(osuWebApi.getUser(info["user"]["id"])[0])

    handleThread = backgroundTaskQueue.createTaskWithNewThread(_loginHandle, 0, username, password, quid, isRemember)


def _loginHandle(username, password, quid, isRemember):
    q = backgroundTaskQueue.findQueue(quid)
    info: dict = q.get()["user"]
    info2: dict = q.get()["user"]

    for k, v in info2.items():
        info.update({k: v})

    # change loggedUser status
    loggedUser.isLogged = True
    loggedUser.userInfo = LoginUserModel(**info)
    loggedUser.lastUpdate = getNowUnixTimestamp()

    # change avatar and username in interface
    signalBus.usernameUpdate.emit(info["username"])
    avatarDownload(info["avatar_url"])

    if isRemember:
        # pickle username and password to local data
        pickle.dump((username, password), open(DataFilePath.userLoginInfo, "wb"))

    # done queue task
    q.task_done()
