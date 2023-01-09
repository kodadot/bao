from aiohttp import ClientSession, FormData
from logging import info, warn
from cloudflare.rest import delete_file_async, post_file_async
from cloudflare.headers import CF_IMAGES_URI, HEADERS
from hypercasual.utils.save import save_file
from hypercasual.very_async.wrapper import Semaphore


async def fetch(session, url):
    async with session.get(url) as response:
        return {
          'type': response.headers['Content-Type'],
          'value': await response.read()
        } 

async def post(session, url, body):
    async with session.post(url, json=body) as response:
        return response


async def post_to_cf(value):
  name, content, type, original_id = value
  info(f'[🗂 ]: Processing {name}')
  # files = {'file': (name, content, type)}
  form = FormData()
  form.add_field("file", content, filename=name, content_type=type)
  # add id to the form
  form.add_field("id", original_id)
  res = await post_file_async(CF_IMAGES_URI, form, headers=HEADERS, name=name)
  if res is None:
    warn(f'[🔴]: NO {name}')
  else:
    info(f'[💚]: OK {res}')

async def make_it_to_cf(name, content):
  id, suffix = name.split('.')
  type = f'image/{suffix}'
  await post_to_cf((name, content, type, id))

async def remove_it_from_cf(item):
  id = item['key']
  url = CF_IMAGES_URI + '/' + id
  info(f'[🌎]: Removing {id}')
  await delete_file_async(url, HEADERS, id)

async def fetch_one(item):
  async with ClientSession() as session:
    info(f'[🌎]: Fetching {item["id"]}')
    res = await fetch(session, item['url'])
  type = res['type']
  suffix = type.split('/')[1]
  name = item['id'] + '.' + suffix
  content = res['value']
  save_file(name, content, 'merger/res/')
  # semaphore = Semaphore.getInstance()
  # semaphore.add(post_to_cf((name, content, type, item['id'])))
