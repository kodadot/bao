
import asyncio
from json import load
from dotenv import load_dotenv
from os import getenv, getcwd
from sys import argv, path
path.append(getcwd())

from logging import info, basicConfig, INFO
from signal import signal, SIGINT
from hypercasual.utils.save import read_file

from hypercasual.very_async.exec import dispatch
from hypercasual.very_async.wrapper import Semaphore
from merger.fetch import fetch_one, make_it_to_cf, remove_it_from_cf

load_dotenv()

START_AT = int(getenv('START_AT')) if getenv('START_AT') else 4
OFFSET = int(getenv('OFFSET')) if getenv('OFFSET') else 2

def handle_sigint(signal_received, frame):
  print('\n\nSIGINT or CTRL-C detected. Exiting gracefully')
  exit(0)

signal(SIGINT, handle_sigint)


async def init_chunk_list_to_file():
  count = int(argv[1]) if len(argv) > 1 else 0
  for i in range(count, count + 2):
    with open(f'merger/meta/chunk{i}.json') as f:
      meta = load(f)
      info(f'[ASYNC INIT]: 🎲 Starting at {i}')
      sem = Semaphore.getInstance()
      for item in meta:
        sem.add(fetch_one(item))

async def init_file_list_to_cf():
  count = int(argv[1]) if len(argv) > 1 else 0
  with open(f'merger/chunk/chunk{count}.txt') as f:
    files = [line.rstrip() for line in f.readlines()]
    for i in files:
      file = read_file(f'merger/res/{i}')
      info(f'[ASYNC INIT]: 🎲 Starting at {i}')
      sem = Semaphore.getInstance()
      sem.add(make_it_to_cf(i, file))


      # ipfs-to-cf-images/missing/chunk2.json

async def init_removal_from_cf():
  count = int(argv[1]) if len(argv) > 1 else 0
  with open(f'ipfs-to-cf-images/missing/chunk{count}.json') as f:
    meta = load(f)
    info(f'[ASYNC INIT]: 🎲 Starting at {count}')
    sem = Semaphore.getInstance()
    for item in meta:
      sem.add(remove_it_from_cf(item))

if __name__ == '__main__':
  basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=INFO, datefmt='%H:%M:%S')
  # raiseExceptions = False # only for the runner
  info('[APP]: Running')
  asyncio.run(dispatch(init_removal_from_cf), debug=True)