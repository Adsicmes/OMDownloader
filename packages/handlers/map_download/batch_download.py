import json
import os.path
import queue
import secrets
import shutil
import time
import uuid
from os import PathLike
from typing import Tuple

import httpx
import i18n
from loguru import logger

from packages.common import backgroundTaskQueue, osuWebApi, retry, taskList
from packages.common.filepath import CacheFilePath, OSUPath
from packages.common.task_queue import beatmapDownloadQueue
from packages.config import config
from packages.model.map_download_model.batch_download_model import DownloadParams
from packages.utils.osu_db.osu_db import OsuDb
from packages.utils.path import isValidLocalPath, convertToValidFilename


def batch_download_exec(params: DownloadParams):
    logger.info("Add batch map download task.")
    handleThread = taskList.add(
        _handle,
        i18n.t("app.tasks.batchMapDownload").replace("{{count}}", str(params["count"])),
        params
    )


def _handle(params: DownloadParams, taskQ: queue.Queue):
    taskQ.put((0, "Starting to read osu db and scrape beatmaps..."))

    totalProgress = 100 if params["isExportOnly"] else 20

    quidSearch = backgroundTaskQueue.createQueue()
    quidResult = backgroundTaskQueue.createQueue()
    quidHandle = backgroundTaskQueue.createQueue()
    searchThread = backgroundTaskQueue.createTaskWithNewThread(_search, 0, params, quidSearch, quidHandle, quidResult,
                                                               taskQ)
    resultThread = backgroundTaskQueue.createTaskWithNewThread(_result, 0, quidSearch, quidHandle, quidResult, params,
                                                               taskQ, totalProgress)

    q = backgroundTaskQueue.findQueue(quidHandle)
    result = q.get()
    q.task_done()

    if params["isExportOnly"]:
        logger.info("Beatmap export only...")
        if not os.path.isdir(params["specifiedPath"]):
            os.makedirs(params["specifiedPath"])

        with open(params["specifiedPath"], "w") as f:
            json.dump(result, f)
            logger.success("Exported. Batch download finished.")
        return

    logger.info(f"Got {len(result)} beatmapsets. Starting download...")
    taskQ.put((totalProgress, "Downloading beatmaps..."))
    time.sleep(1)

    downloadThread = backgroundTaskQueue.createTaskWithNewThread(_download, None, params, result, taskQ)


@retry(delays=(1 for _ in range(int(config["Retry.ppy_sh"]))), exceptions=(httpx.HTTPError,))
def _requestSearch(params: DownloadParams):
    pm = params["official"]
    pm_q = ""

    pm_q += f"ar>={params['filter']['ar'][0]}  ar<={params['filter']['ar'][1]} " \
        if params['filter']['ar'] else ""
    pm_q += f"od>={params['filter']['od'][0]}  od<={params['filter']['od'][1]} " \
        if params['filter']['od'] else ""
    pm_q += f"cs>={params['filter']['cs'][0]}  cs<={params['filter']['cs'][1]} " \
        if params['filter']['cs'] else ""
    pm_q += f"hp>={params['filter']['hp'][0]}  hp<={params['filter']['hp'][1]} " \
        if params['filter']['hp'] else ""
    pm_q += f"bpm>={params['filter']['bpm'][0]}  bpm<={params['filter']['bpm'][1]} " \
        if params['filter']['bpm'] else ""
    pm_q += f"star>={params['filter']['star'][0]}  star<={params['filter']['star'][1]} " \
        if params['filter']['star'] else ""
    pm_q += f"length>={params['filter']['length'][0]}  length<={params['filter']['length'][1]} " \
        if params['filter']['length'] else ""
    rankedParam = params['filter']['ranked']
    pm_q += f"ranked>={rankedParam[0][0]}{str(rankedParam[0][1]).zfill(2)}{str(rankedParam[0][2]).zfill(2)} " \
            f"ranked<={rankedParam[1][0]}{str(rankedParam[1][1]).zfill(2)}{str(rankedParam[1][2]).zfill(2)} " \
        if params['filter']['ranked'] else ""
    createdParam = params['filter']['created']
    pm_q += f"created>={createdParam[0][0]}{str(createdParam[0][1]).zfill(2)}{str(createdParam[0][2]).zfill(2)} " \
            f"created<={createdParam[1][0]}{str(createdParam[1][1]).zfill(2)}{str(createdParam[1][2]).zfill(2)} " \
        if params['filter']['created'] else ""

    pm_q += params['official']['q']

    pm["q"] = pm_q
    return osuWebApi.searchBeatmaps(pm)


def _search(params: DownloadParams, quidSearch: uuid.UUID, quidHandle: uuid.UUID, quidResult: uuid.UUID,
            taskQ: queue.Queue):
    qSearch = backgroundTaskQueue.findQueue(quidSearch)
    qResult = backgroundTaskQueue.findQueue(quidResult)

    tryCount = 0
    while True:
        if tryCount >= int(config["Retry.ppy_sh"]):
            raise httpx.RequestError("Too many request failed when request beatmaps.")

        if not qSearch.get():  # stop when get False
            break
        # noinspection PyCallingNonCallable
        resp = _requestSearch(params)
        if resp.status_code == httpx.codes.OK:
            qResult.put(resp.json())
            continue

        tryCount += 1

    qSearch.task_done()


def _result(quidSearch: uuid.UUID, quidHandle: uuid.UUID, quidResult: uuid.UUID,
            params: DownloadParams, taskQ: queue.Queue, totalProgress: int):
    qSearch = backgroundTaskQueue.findQueue(quidSearch)
    qResult = backgroundTaskQueue.findQueue(quidResult)
    results = []

    taskQ.put((0, "Reading osu db..."))
    osuDb = OsuDb(OSUPath.osuDbPath)
    beatmapExists = osuDb.getAllBeatmapsetIds()

    taskQ.put((5, "Scraping beatmaps..."))
    qSearch.put(True)
    while True:
        result: dict = qResult.get()

        isBreak = False
        for bm in result["beatmapsets"]:
            if bm["id"] in beatmapExists:
                continue

            results.append(bm)

            taskQ.put((int(totalProgress * (len(results) / params["count"])),
                       f"Got {len(results)} of {params['count']} beatmaps info."))

            if len(results) >= params["count"]:
                isBreak = True
                break
        if isBreak:
            break

        if result["cursor_string"] is None:
            break

        params["official"]["cursor_string"] = result["cursor_string"]
        qSearch.put(True)

    qSearch.put(False)
    qResult.task_done()
    backgroundTaskQueue.findQueue(quidHandle).put(results)


def _download(params: DownloadParams, result: list, taskQ: queue.Queue):
    total_count = len(result)
    downloadListQueue = queue.Queue()
    downloadOutputQueue = queue.Queue()

    downloadPath = params["specifiedPath"] if isValidLocalPath(params["specifiedPath"]) else OSUPath.songPath
    cacheFolder = os.path.join(CacheFilePath.mapDownloadPath, secrets.token_urlsafe(16))
    if not os.path.isdir(cacheFolder):
        os.makedirs(cacheFolder)

    for i in range(total_count):
        beatmap_info = result[i]
        bmsid = beatmap_info["id"]
        fp = os.path.join(
            cacheFolder,
            convertToValidFilename(f"{bmsid} {beatmap_info['artist']} - {beatmap_info['title']}.osz")
        )
        nv = params["noVideo"]

        downloadListQueue.put((_beatmapsetsDownload, ((bmsid, fp, nv), downloadPath)))

    beatmapDownloadQueue.startQueue(downloadListQueue, downloadOutputQueue)

    while info := downloadOutputQueue.get():
        info: Tuple[int, int, Tuple[Tuple[int, PathLike, bool], PathLike]]
        total, done, args = info
        logger.info(f"{args[0][0]} downloaded. {done} of {total} Total.")
        taskQ.put((done / total * 80 + 20, f"Beatmapset {args[0][0]} downloaded. {done} of {total} Total."))
        if total == done:
            taskQ.put((done / total * 80 + 20, f"Downloaded {done} of {total} beatmaps."))
            break

    logger.success("Batch download finished.")


@retry(delays=(1 for _ in range(int(config["Retry.ppy_sh"]))), exceptions=(httpx.HTTPError,))
def _beatmapsetsDownload(dlFuncParam: Tuple[int, PathLike, bool], targetPath: PathLike):
    bmsid, fp, nv = dlFuncParam
    osuWebApi.downloadBeatmapset(bmsid, fp, nv)
    if os.path.isfile(os.path.join(targetPath, os.path.basename(fp))):
        os.remove(os.path.join(targetPath, os.path.basename(fp)))
    shutil.move(fp, targetPath)
