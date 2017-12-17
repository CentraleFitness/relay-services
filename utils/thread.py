import concurrent.futures
from queue import Queue


class ThreadStatus(Enum):
    STOPPED = 0
    RUNNING = 1


class ThreadController():
    def __init__(self, *args, **kwargs):
        self.workers = kwargs.get('max_workers', 3)
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=self.workers)
        self.futures = dict()
        self.status = dict()
        self.queue = Queue()
        self.last_thread_id = 0x00

    def __getitem__(self, item):
        return self.status[item]

    def _get_id(self):
        self.last_thread_id += 1
        return self.last_thread_id - 1

    def start(self, func, *args, **kwargs):
        if isinstance(kwargs.get('factory', None), (list, tuple)):
            for t_args in kwargs['factory']:                   
                id = self._get_id()
                self.futures[id] = self.executor.submit(func, id, self, *t_args)
                self.status[id] = ThreadStatus.RUNNING
        else:
            id = self._get_id()
            self.futures[id] = self.executor.submit(func, id, self, *args)
            self.status[id] = ThreadStatus.RUNNING

    def stop(self, thread_id):
        self.status[thread_id] = ThreadStatus.STOPPED

    def stop_all(self):
        for thread in self.status:
            self.status[thread] = ThreadStatus.STOPPED
