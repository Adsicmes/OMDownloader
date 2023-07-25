import threading
from queue import Queue
from typing import Tuple, Callable, Any

from PySide6.QtCore import QObject


class TaskManager(QObject):

    def __init__(self, limit):
        super().__init__()
        self.limit = limit
        self.semaphore = threading.Semaphore(limit)
        self.queues = {}

    def startQueue(self, qIn: Queue[Tuple[Callable, Tuple]],
                   qOut: Queue[Tuple[int, int, Tuple[Any, ...]]]):
        self.queues[str(qIn)] = {}
        self.queues[str(qIn)]["totalCount"] = qIn.qsize()
        self.queues[str(qIn)]["doneCount"] = 0
        for _ in range(self.limit):
            threading.Thread(target=self.worker, args=(qIn, qOut)).start()

    def worker(self, qIn: Queue[Tuple[Callable, Tuple]],
               qOut: Queue[Tuple[int, int, Tuple[Any, ...]]]):
        while True:
            self.semaphore.acquire()
            if qIn.empty():
                self.semaphore.release()
                break
            else:
                item = qIn.get()
            self.processItem(item, qIn, qOut)
            self.semaphore.release()

    def processItem(self, item: Tuple[Callable, Tuple],
                    qIn: Queue[Tuple[Callable, Tuple]],
                    qOut: Queue[Tuple[int, int, Tuple[Any, ...]]]):
        func, args = item
        thread = threading.Thread(target=self.run, args=(func, args, qIn, qOut))
        thread.start()
        thread.join(timeout=0)

    def run(self, func: Callable, args: Tuple[Any, ...],
            qIn: Queue[Tuple[Callable, Tuple]],
            qOut: Queue[Tuple[int, int, Tuple[Any, ...]]]):
        func(*args)

        self.queues[str(qIn)]["doneCount"] += 1
        total: int = self.queues[str(qIn)]["totalCount"]
        done: int = self.queues[str(qIn)]["doneCount"]
        qOut.put((total, done, args))

        if total == done:
            qIn.task_done()
            self.queues.pop(str(qIn))
