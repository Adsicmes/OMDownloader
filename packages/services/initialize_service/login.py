import os
import pickle

from loguru import logger

from packages.common import DataFilePath
from packages.handlers.account.osu.login import login_exec


def initLogin():
    if os.path.isfile(DataFilePath.userLoginInfo):
        logger.info("Detected local user login info, loading and logining...")
        username, account = pickle.load(open(DataFilePath.userLoginInfo, "rb"))
        login_exec(username, account)
