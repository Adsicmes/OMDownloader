from packages.model.map_download_model.batch_download_model import DownloadParams


def batch_download_exec(params: DownloadParams):
    pass
#     handleThread = taskQueue.createTaskWithNewThread(_handle, 0, params)
#
#
# def _handle(params: DownloadParams):
#     quid = taskQueue.createQueue()
#     params, resultList = taskQueue.findQueue(quid).get()
#     searchThread = taskQueue.createTaskWithNewThread(_search, 0, params, quid)
#     resultThread = taskQueue.createTaskWithNewThread(_result, 0, quid, params["count"])
#     taskQueue.findQueue(quid).task_done()
#
#
# @retry((httpx.HTTPError,), tries=config["retry"]["ppy_sh"], delay=1, logger=logger)
# def _search(params: DownloadParams, quid: uuid.UUID):
#     q = taskQueue.findQueue(quid)
#
#     while True:
#         if not q.get():  # stop when get False
#             break
#         resp = osuWebApi.searchBeatmaps(params["official"])
#         if resp.status_code == 200:
#             q.put(resp.json())
#
#
# def _result(quid: uuid.UUID, countNeeded: int):
#     q = taskQueue.findQueue(quid)
#     results = []
#
#     while True:
#         if not len(results) <= countNeeded:
#             break
#         results.append(result)
