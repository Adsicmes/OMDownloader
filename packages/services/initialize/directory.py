import os

import win32api
import win32con
from loguru import logger

from packages.config import config


def initDir():
    for d in [
        config["Others.cacheLocation"],
        config["Others.dataLocation"],
        config["Others.langLocation"],
        os.path.join(config["Others.cacheLocation"], "mapDownload")
    ]:
        if not os.path.isdir(d):
            os.mkdir(d)
            logger.info(f"Successfully create directory: {d}")


def initOsuDir():
    key = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT,
                              'osu\\DefaultIcon', 0, win32con.KEY_READ)
    osu = win32api.RegQueryValue(key, '')
    osu: list = str(osu).split("\"")[1].split("\\")
    del osu[-1]
    osu[0] += r"\\"

    config.setValue("Others", "osuPath", os.path.join(*osu), saveToFile=False)
