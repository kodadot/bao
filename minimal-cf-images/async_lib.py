import asyncio
from logging import warn
from signal import raise_signal, SIGINT
from limited_dispatch import LimitedDispatch

async def dispatch(init):
    await init()

    ld = LimitedDispatch.getInstance()

    await ld.join()

async def dirty_exit():
    sleep_for = 50
    warn(f'⚠️⚠️ [APP]: will be dead in {sleep_for} sec ⚠️⚠️')
    await asyncio.sleep(sleep_for) # 5 minutes
    raise_signal(SIGINT)
