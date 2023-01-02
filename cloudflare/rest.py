from aiohttp import ClientSession, FormData
from logging import info, warning
from headers import HEADERS

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
        warning(f'[🔥❌]: {name} https://http.cat/{response.status}')
        return None

async def post_file_async(url, body, headers=HEADERS, name=''):
  async with ClientSession() as session:
    res = await post_file(session, url, body, headers, name)
    return res


