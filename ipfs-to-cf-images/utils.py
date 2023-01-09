from logging import info, warn
from collections import namedtuple
from aiohttp import ClientSession, FormData
from requests import post as post_request
from headers import CF_IMAGES_URI, HEADERS
from my_queue import add_task

PINATA_BASE_API = "https://kodadot.mypinata.cloud/"
IPFS_PREFIX = "ipfs://"
FULL_IPFS_PREFIX = "ipfs://ipfs/"

CF_DURABLE_OBJECT = "https://durable-jpeg.kodadot.workers.dev"

def map_to_kv(meta):
  return {
    'id': unwrap_or_default(meta['image'], '').replace(FULL_IPFS_PREFIX, ""),
    'value': unwrap_or_default(meta['image'], '').replace(IPFS_PREFIX, PINATA_BASE_API),
  }

def unwrap_or_default(value, default):
  if value is None:
    return default
  return value

def only_with_value(meta):
  return meta['value'] != ''

async def fetch(session, url):
    async with session.get(url) as response:
        return {
          'type': response.headers['Content-Type'],
          'value': await response.read()
        } 

async def post(session, url, body):
    async with session.post(url, json=body) as response:
        return response   

async def post_file(session, url, body, headers=HEADERS, name=''):
  async with session.post(url, data=body, headers=headers) as response:
      if response.status == 200:
        info(f'[ASYNC 🔥]: {response.status} {name}')
        val = await response.json()
        return val['result']['id']
      else: 
        warn(f'[🔥❌]: {name} https://http.cat/{response.status}')
        return None


def post_file_sync(url, body, headers=HEADERS, name=''):
  res = post_request(url, data=body, headers=headers)
  if res.status_code == 200:
    info(f'[🔥]: {res.status_code} {name}')
    val = res.json()
    return val['result']['id']
  else: 
    info(f'[🔥❌]: {type} https://http.cat/{res.status_code}')
    return None

async def post_file_async(url, body, headers=HEADERS, name=''):
  async with ClientSession() as session:
    res = await post_file(session, url, body, headers, name)
    return res

Task = namedtuple("Task", ['handler','value'])

def save_file(file_name, data, path='./'):
  with open(path + file_name, 'wb') as outfile:
    outfile.write(data)

async def fetch_one(item):
  async with ClientSession() as session:
    info(f'[🌎]: Fetching {item["id"]}')
    res = await fetch(session, item['value'])
    type = res['type']
    suffix = type.split('/')[1]
    name = item['id'] + '.' + suffix
    content = res['value']
    save_file(name, content, 'res/')
    await add_task(map_post_to_cf((name, content, type, item['id'])))

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
  

async def store_to_durable_object(kv):
  async with ClientSession() as session:
    res = await post(session, CF_DURABLE_OBJECT + '/upload', kv)
    key = kv['key']
    info(f'[ASYNC OBJECT]: ❄️  {res.status} {key}')

def map_fetch_one(item):
  return Task(fetch_one, item)

# name, value, type, original_id
def map_post_to_cf(maker):
  return Task(post_to_cf, maker)

# Item should be key-value object
def map_to_durable_object(item):
  return Task(store_to_durable_object, item)

def map_kb_to_tuple(item):
  return (item['key'], item['value'])
