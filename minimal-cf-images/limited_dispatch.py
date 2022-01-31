import asyncio


class LimitedDispatch:
    _instance = None

    def getInstance(*args, **kwargs):
        if LimitedDispatch._instance is None:
            LimitedDispatch._instance = LimitedDispatch.__LimitedDispatch(*args, **kwargs)
        return LimitedDispatch._instance

    class __LimitedDispatch:
        def __init__(self, max_tasks=20):
            self._max_tasks = max_tasks
            self._tasks = set()
            self._lock = asyncio.Condition()
            self._queue = asyncio.Queue()

        async def add(self, async_item_factory):
            async with self._lock:
                if self._max_tasks > len(self._tasks):
                    self._spawn(async_item_factory)
                else:
                    await self._queue.put(async_item_factory)

        async def _task_done(self, task):
            async with self._lock:
                self._tasks.discard(task)
                assert self._max_tasks > len(self._tasks)
                try:
                    aif = self._queue.get_nowait()
                    self._spawn(aif)
                except asyncio.QueueEmpty:
                    pass
                self._lock.notify_all()

        async def join(self):
            async with self._lock:
                while len(self._tasks) > 0 and self._queue.qsize() > 0:
                    await self._lock.wait()

        def _spawn(self, async_item_factory):
            task = asyncio.get_running_loop().create_task(async_item_factory)
            self._tasks.add(task)
            task.add_done_callback(lambda X: asyncio.get_running_loop().create_task(self._task_done(X)))
