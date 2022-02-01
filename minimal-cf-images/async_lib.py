import asyncio
import logging
from logging import warning
from signal import raise_signal, SIGINT


async def dispatch(init):
    await init()

    while True:
        pending = asyncio.all_tasks() - {asyncio.current_task()}
        logging.debug("dispatch(): num of pending tasks=%d"%len(pending))
        if len(pending) <= 0:
            break
        await asyncio.gather(*pending)


async def dirty_exit():
    sleep_for = 50
    warning(f'⚠️⚠️ [APP]: will be dead in {sleep_for} sec ⚠️⚠️')
    await asyncio.sleep(sleep_for) # 5 minutes
    raise_signal(SIGINT)
