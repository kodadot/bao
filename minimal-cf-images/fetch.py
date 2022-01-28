from aiohttp import ClientSession, FormData
from logging import info, warn
from constants import CF_DURABLE_OBJECT, SUBSQUID_API
from graphql import last_minted_query
from headers import CF_IMAGES_URI, HEADERS

from my_queue import add_task
from tasks import Task


async def post_file(session, url, body, headers=HEADERS, name=''):
  async with session.post(url, data=body, headers=headers) as response:
      if response.status == 200:
        info(f'[ASYNC 🔥]: {response.status} {name}')
        val = await response.json()
        return val['result']['id']
      else: 
        warn(f'[🔥❌]: {name} https://http.cat/{response.status}')
        return None

async def post_file_async(url, body, headers=HEADERS, name=''):
  async with ClientSession() as session:
    res = await post_file(session, url, body, headers, name)
    return res

async def post(session, url, body):
    async with session.post(url, json=body) as response:
        return response

async def store_to_durable_object(kv):
  async with ClientSession() as session:
    res = await post(session, CF_DURABLE_OBJECT + '/upload', kv)
    key = kv['key']
    info(f'[ASYNC OBJECT]: ❄️  {res.status} {key}')

async def post_to_cf(value):
  name, content, type, original_id = value
  info(f'[🗂 ]: Processing {name}')
  # files = {'file': (name, content, type)}
  form = FormData()
  form.add_field("file", content, filename=name, content_type=type)
  res = await post_file_async(CF_IMAGES_URI, form, headers=HEADERS, name=name)
  kv = {
    'key': original_id,
    'value': res
  }
  if (res is not None): 
    await add_task(map_to_durable_object(kv))

async def fetch_last_minted_nfts():
  kv = last_minted_query()
  async with ClientSession() as session:
    res = await post(session, SUBSQUID_API, kv)
    data = await res.json()
    return data['data']['nFTEntities']

# name, value, type, original_id
def map_post_to_cf(maker):
  return Task(post_to_cf, maker)

# Item should be key-value object
def map_to_durable_object(item):
  return Task(store_to_durable_object, item)