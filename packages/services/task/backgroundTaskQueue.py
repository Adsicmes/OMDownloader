import uuid
from queue import Queue
from threading import Thread
from typing import Callable, List, Tuple


class BackgroundTaskQueue:
    def __init__(self):
        self.taskList: List[Thread] = []
        self.queueList: List[Tuple[uuid.UUID, Queue]] = []

    def createTaskWithNewThread(self, func: Callable, timeout=None, *args, **kwargs) -> Thread:
        t = Thread(target=func, args=args, kwargs=kwargs, daemon=True)
        self.taskList.append(t)
        t.start()
        t.join(timeout)
        return t

    def createQueue(self):

        q = Queue()
        quid = uuid.uuid4()
        self.queueList.append((quid, q))
        return quid

    def findQueue(self, quid: uuid.UUID) -> Queue:
        for q in self.queueList:
            if q[0] == quid:
                return q[1]
