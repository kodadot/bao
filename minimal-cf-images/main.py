
import asyncio
from logging import info, basicConfig, INFO, raiseExceptions
from async_lib import dispatch
from fetch import fetch_last_minted_nfts, fetch_one
from signal import signal, SIGINT
from limited_dispatch import LimitedDispatch

def handle_sigint(signal_received, frame):
  print('\n\nSIGINT or CTRL-C detected. Exiting gracefully')
  exit(0)

signal(SIGINT, handle_sigint)


async def async_init():
  meta = await fetch_last_minted_nfts()
  ld = LimitedDispatch.getInstance()
  for item in meta:
    await ld.add(fetch_one(item))
    #await add_task(map_fetch_one(item), jozo)

if __name__ == '__main__':
  basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=INFO, datefmt='%H:%M:%S')
  # raiseExceptions = False # only for the runner
  info('[APP]: Running')
  asyncio.run(dispatch(async_init), debug=True)