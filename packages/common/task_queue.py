from packages.services.task.backgroundTaskQueue import BackgroundTaskQueue
from packages.services.task.taskList import TaskList
from packages.services.task.taskManager import TaskManager

backgroundTaskQueue = BackgroundTaskQueue()
taskList = TaskList()

beatmapDownloadQueue = TaskManager(10)
