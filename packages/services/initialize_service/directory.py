import os

from loguru import logger

from packages.config import config


def initDir():
    for d in [
        config["others"]["cacheLocation"],
        config["others"]["dataLocation"],
        config["others"]["langLocation"],
    ]:
        if not os.path.isdir(d):
            os.mkdir(d)
            logger.info(f"Successfully create directory: {d}")
