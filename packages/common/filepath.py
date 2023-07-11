import os

from packages.config import config


class DataFilePath:
    basePath = config["others"]["dataLocation"]
    userLoginInfo = os.path.join(config["others"]["dataLocation"], "userLoginInfo.pk")


class CacheFilePath:
    basePath = config["others"]["cacheLocation"]
