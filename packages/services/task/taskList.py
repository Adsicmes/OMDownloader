import secrets
from queue import Queue
from threading import Thread
from typing import Callable, List

from PySide6.QtCore import QObject, Signal


class Task(QObject):
    _uid: str
    name: str

    _func: Thread
    _q: Queue

    progress: int = 0
    msg: str = ""

    progressUpdate = Signal(int)
    msgUpdate = Signal(str)

    def __init__(self, func: Callable, name: str = None, *args, **kwargs):
        super().__init__()
        self._q = Queue()
        kwargs.update({'taskQ': self._q})
        self._func = Thread(target=func, args=args, kwargs=kwargs, daemon=True)
        self.name = name
        self._uid = secrets.token_urlsafe(16)

    def start(self):
        self._func.start()
        self._func.join(timeout=0)
        trackThread = Thread(target=self._track, daemon=True)
        trackThread.start()
        trackThread.join(timeout=0)

    def isAlive(self):
        return self._func.is_alive()

    def _track(self):
        while True:
            progress, msg = self._q.get()
            self.progress = progress
            self.msg = msg
            self.progressUpdate.emit(progress)
            self.msgUpdate.emit(msg)

            if not self._func.is_alive():
                self._q.task_done()
                self.msgUpdate.emit("Done")
                self.progressUpdate.emit(100)
                break

    @property
    def thr(self) -> Thread:
        return self._func

    @property
    def queue(self) -> Queue:
        return self._q

    @property
    def uid(self) -> str:
        return self._uid


class TaskList(QObject):
    tasks: List[Task] = []

    taskStatUpdate = Signal()

    def __init__(self):
        super().__init__()

    def __getitem__(self, uid):
        for task in self.tasks:
            if task.uid == uid:
                return task

    def add(self, func: Callable, name: str = None, *args, **kwargs):
        task = Task(func, name, *args, **kwargs)
        self.tasks.append(task)
        self.taskStatUpdate.emit()
        return task.uid

    def start(self, uid):
        self[uid].start()

    def remove(self, uid):
        task = self[uid]
        if not task.isAlive():
            self.tasks.remove(self[uid])
            self.taskStatUpdate.emit()
            return True
        else:
            return False

    def removeDone(self):
        for task in self.tasks:
            if task.isAlive():
                continue
            self.tasks.remove(task)
        self.taskStatUpdate.emit()
