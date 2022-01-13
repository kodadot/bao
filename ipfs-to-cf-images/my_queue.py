
from asyncio import Queue

jozo = Queue()

async def add_to_queue(tasks):
  for task in tasks:
      await jozo.put(task)

async def add_task(task):
  await jozo.put(task)