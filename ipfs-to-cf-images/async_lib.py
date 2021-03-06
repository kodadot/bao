import asyncio


async def dispatch(runner):
    queue = asyncio.Queue()
    await runner(queue)
    limited_set = LimitedSet(maxsize=20, jozo= queue)

    try:
        while not queue.empty():
            task = await queue.get()
            handler = task.handler
            value = task.value
            await limited_set.add(lambda: asyncio.get_running_loop().create_task(handler(value)))
    except asyncio.CancelledError:
        pass  # cleanup before grateful exit
    
    await queue.join()


class LimitedSet(set):
    def __init__(self, *argv, maxsize, jozo):
        super().__init__(*argv)
        self._maxsize = maxsize
        self._lock = asyncio.Condition()
        self.jozo = jozo


    async def add(self, item_factory):
        async with self._lock:
            while self._maxsize <= len(self):
                await self._lock.wait()
            item = item_factory()
            super().add(item)
            item.add_done_callback(lambda X: asyncio.get_running_loop().create_task(self.drop(X)))
            item.add_done_callback(lambda X: self.jozo.task_done())

    async def drop(self, item):
        async with self._lock:
            self.discard(item)
            assert self._maxsize > len(self)
            self._lock.notify_all()