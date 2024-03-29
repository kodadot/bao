from aiohttp import ClientSession, FormData
from logging import info, warning
from cloudflare.rest import post_file_async
from constants import CF_DURABLE_OBJECT, SUBSQUID_API
from graphql import last_minted_query
from headers import CF_IMAGES_URI, HEADERS

from semaphore_wrapper import Semaphore
from utils import map_to_kv, only_with_value


async def fetch(session, url):
    async with session.get(url) as response:
        return {
          'type': response.headers['Content-Type'],
          'value': await response.read()
        } 

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
    semaphore = Semaphore.getInstance()
    semaphore.add(store_to_durable_object(kv))

async def fetch_last_minted_nfts():
  kv = last_minted_query()
  unwrap = lambda x: x['meta']
  async with ClientSession() as session:
    async with session.post(SUBSQUID_API, json=kv) as response:
      val = await response.json()
      data = map(unwrap, val['data']['nftEntities'])
      return list(filter(only_with_value, map(map_to_kv, data)))

async def fetch_one(item):
  async with ClientSession() as session:
    info(f'[🌎]: Fetching {item["id"]}')
    res = await fetch(session, item['value'])
  type = res['type']
  suffix = type.split('/')[1]
  name = item['id'] + '.' + suffix
  content = res['value']
  # save_file(name, content, 'res/')
  semaphore = Semaphore.getInstance()
  semaphore.add(post_to_cf((name, content, type, item['id'])))
