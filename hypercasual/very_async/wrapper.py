import asyncio
import logging
from uuid import uuid4

class Semaphore:
    _instance = None

    def getInstance(*args, **kwargs):
        if Semaphore._instance is None:
            try:
                asyncio.current_task()
            except RuntimeError:
                logging.error("Semaphore.getInstance: please create instance inside event loop.")
                raise
            Semaphore._instance = Semaphore._SemaphoreWrapper(*args, **kwargs)
        return Semaphore._instance

    class _SemaphoreWrapper:
        def __init__(self, size=20):
            self._semaphore = asyncio.BoundedSemaphore(size)

        async def _wait_wrap(self, coroutine_object):
            id = str(uuid4())
            logging.debug("sem._wait_wrap: waiting with %s, id=%s"%(str(coroutine_object), id))
            async with self._semaphore:
                logging.debug("sem._wait_wrap: acquired resource for %s id=%s"%(str(coroutine_object), id))
                await coroutine_object

        def add(self, coroutine_object):
            asyncio.create_task(self._wait_wrap(coroutine_object))
