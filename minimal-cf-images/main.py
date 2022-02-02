
import asyncio
from logging import info, basicConfig, INFO
from async_lib import dispatch
from fetch import fetch_last_minted_nfts, fetch_one
from signal import signal, SIGINT
from semaphore_wrapper import Semaphore

def handle_sigint(signal_received, frame):
  print('\n\nSIGINT or CTRL-C detected. Exiting gracefully')
  exit(0)

signal(SIGINT, handle_sigint)


async def async_init():
  meta = await fetch_last_minted_nfts()
  sem = Semaphore.getInstance()
  for item in meta:
    sem.add(fetch_one(item))

if __name__ == '__main__':
  basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=INFO, datefmt='%H:%M:%S')
  # raiseExceptions = False # only for the runner
  info('[APP]: Running')
  asyncio.run(dispatch(async_init), debug=True)