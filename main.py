import time
import queue
import typing as T
from threading import Thread, current_thread

CALLBACK = T.Callable[..., None]
TASK = T.Tuple[CALLBACK, T.Any, T.Any]
TASKQUEUE = queue.Queue

class Worker(Thread):
    def __init__(self, tasks: queue.Queue[TASK]):
        super().__init__()
        self.tasks = tasks

    def run(self) -> None:
        while True:
            func, args, kwargs = self.tasks.get()
            try:
                func(*args, **kwargs)
            except Exception as err:
                raise err
            else:
                self.tasks.task_done()

class ThreadPool:
    def __init__(self, num_threads:int):
        self.tasks: TASKQUEUE = queue.Queue(num_threads)
        self.num_threads = num_threads

        for _ in range(num_threads):
            worker = Worker(self.tasks)
            worker.daemon = True
            worker.start()

    def submit(self, func: CALLBACK, *args, **kwargs) -> None:
        self.tasks.put((func, args, kwargs))

    def wait(self) -> None:
        self.tasks.join()

def cpu_waster(i:int) -> None:
    name = current_thread().name
    print(f"{name} doing {i} work\n")
    time.sleep(10)

def main() -> None:
    pool = ThreadPool(num_threads=5)
    for i in range(30):
        pool.submit(cpu_waster, i)
    else:
        print("All work requests sent")
        pool.wait()
        print(f"All work completed")

if __name__ == "__main__":
    main()
