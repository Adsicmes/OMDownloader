import queue
import threading

from loguru import logger


class TaskQueue:

    # Constructor, require the task for the queue, the function to finish
    #   the task, and the maximum size of this queue
    def __init__(self, task_name, task_function, max_size):
        self.task_name = task_name
        self.task_function = task_function
        self.task_queue = queue.Queue(max_size)

    # Adding a task to the queue. This function returns 1 if the task is
    #   successfully added to the queue, 2 if the queue is full, 0 if
    #   some other kind of error occurs
    def add(self, *args, **kwargs):
        added = 0

        try:
            self.task_queue.put_nowait((args, kwargs))
            added = 1
            logger.info("")
        except Exception as queue.Full:
            added = 2
            print("任务队列已满！")
        except:
            print("未知错误发生！")

        return added

    def __perform_task(self):
        while True:
            try:
                item = self.task_queue.get_nowait()
                print(f'正在执行{item}')
                self.task_function(item)
                print(f'结束执行{item}')
            except Exception as queue.Empty:
                print("队列任务空！注释此行代码以停止显示")
            except:
                print("未知错误发生！")

    def perform_task(self):
        threading.Thread(target=self.__perform_task(), daemon=True).start()

    def save_task(self):
        ...
