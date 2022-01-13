import asyncio
from my_queue import jozo


async def dispatch(runner):
    await runner()
    limited_set = LimitedSet(maxsize=20)

    try:
        while True:
            # recursion
            # item should be url, handler async 
            if not jozo.empty():
                task = await jozo.get()
                handler = task.handler
                value = task.value
                await limited_set.add(lambda: asyncio.get_event_loop().create_task(handler(value)))
            
            pass  # actual work
    except asyncio.CancelledError:
        pass  # cleanup before grateful exit
    
    await jozo.join()


class LimitedSet(set):
    def __init__(self, *argv, maxsize):
        super().__init__(*argv)
        self._maxsize = maxsize
        self._has_space_fut = asyncio.Future()
        self._has_space_fut.set_result(True)

    async def add(self, item_factory):
        # only one coro should wait on this future
        await self._has_space_fut
        item = item_factory()
        super().add(item)
        item.add_done_callback(lambda X: self.discard(X))
        item.add_done_callback(lambda X: jozo.task_done())
        if self._maxsize < len(self):
            self._has_space_fut = asyncio.Future()

    def discard(self, item):
        super().discard(item)
        if len(self) < self._maxsize and not self._has_space_fut.done():
            self._has_space_fut.set_result(True)