import asyncio
from json import load
from dog import store_to_durable_object
from dotenv import load_dotenv
from os import getenv
from logging import info, basicConfig, INFO
from signal import signal, SIGINT
from async_lib import dispatch
from my_queue import add_task
from sync_lib import fetch_all

from utils import map_fetch_one, map_post_to_cf, only_with_value, map_to_kv

load_dotenv()

START_AT = int(getenv('START_AT')) if getenv('START_AT') else 0
OFFSET = int(getenv('OFFSET')) if getenv('OFFSET') else 2

def handle_sigint(signal_received, frame):
  print('\n\nSIGINT or CTRL-C detected. Exiting gracefully')
  exit(1)

signal(SIGINT, handle_sigint)


def init():
  for i in range(START_AT, START_AT + OFFSET):
    with open(f'meta/chunk{i}.json') as f:
      info(f'[INIT]: 🎲 Starting at {i} of {START_AT + OFFSET}')
      meta = load(f)
      final = fetch_all(meta)
      store_to_durable_object(final)
      info(f'[CHUNK]: ✅ {i}')

async def async_init():
  for i in range(START_AT, START_AT + OFFSET):
    with open(f'missing/chunk{i}.json') as f:
      info(f'[ASYNC INIT]: 🎲 Starting at {i} of {START_AT + OFFSET}')
      meta = load(f)
      # mapped = list(map(map_fetch_one, meta))
      for item in meta:
        await add_task(map_fetch_one(item))
      # await add_to_queue(list(map(map_fetch_one, meta)))

  

def full_init():
  with open('meta.json') as meta_file:
      meta = load(meta_file)
      unwrapped = meta['data']['meta']
      processed = list(filter(only_with_value, map(map_to_kv, unwrapped)))
      all = fetch_all(processed)
      info(f'[DONE]: Processing {len(all)} items')
      # return post_to_cf(all)

async def async_last_init():
  with open('res.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
      p = line.strip().replace('./', 'opt/res/')
      with open(p, 'rb') as f:
        content = f.read()
        name = p.replace('opt/res/', '')
        type = 'image/' + name.split('.')[-1]
        id = name.split('.')[0]
        await add_task(map_post_to_cf((name, content, type, id)))

if __name__ == '__main__':
  basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=INFO, datefmt='%H:%M:%S')
  info('[APP]: Running')
  asyncio.run(dispatch(async_init), debug=True)