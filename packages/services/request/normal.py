from io import BytesIO

import httpx
from PIL import Image

from packages.common import retry
from packages.common import signalBus, backgroundTaskQueue, CacheFilePath
from packages.config import config


# noinspection DuplicatedCode
def avatarDownload(url):
    task = backgroundTaskQueue.createTaskWithNewThread(_avatarDownload, 0, url)


@retry(delays=(1 for _ in range(int(config["Retry.ppy_sh"]))), exceptions=(httpx.HTTPError,))
def _avatarDownload(url):
    image = Image.open(BytesIO(httpx.get(url).content))
    image.save(CacheFilePath.avatarPath)
    signalBus.avatarUpdate.emit(CacheFilePath.avatarPath)


# noinspection DuplicatedCode
def coverDownload(url):
    task = backgroundTaskQueue.createTaskWithNewThread(_coverDownload, 0, url)


@retry(delays=(1 for _ in range(int(config["Retry.ppy_sh"]))), exceptions=(httpx.HTTPError,))
def _coverDownload(url):
    image = Image.open(BytesIO(httpx.get(url).content))
    image.save(CacheFilePath.coverPath)
    signalBus.coverUpdate.emit(CacheFilePath.coverPath)
