
import asyncio
from logging import info, basicConfig, INFO
from async_lib import dispatch
from my_queue import add_task

async def async_init(jozo):
  pass
  # for i in range(START_AT, START_AT + OFFSET):
  #   with open(f'missing/chunk{i}.json') as f:
  #     meta = load(f)
  #   info(f'[ASYNC INIT]: 🎲 Starting at {i} of {START_AT + OFFSET}')
  #   # mapped = list(map(map_fetch_one, meta))
  #   for item in meta:
  #       await add_task(map_fetch_one(item), jozo)

if __name__ == '__main__':
  basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=INFO, datefmt='%H:%M:%S')
  info('[APP]: Running')
  asyncio.run(dispatch(async_init), debug=True)