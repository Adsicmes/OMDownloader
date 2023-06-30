from loguru import logger

from packages.utils import getNowUnixTimestamp


def initLogger():
    logger.add(rf"log\debug_{getNowUnixTimestamp()}.log", enqueue=True, backtrace=True, diagnose=True)
