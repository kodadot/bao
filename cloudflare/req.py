from logging import info
from requests import post as post_request
from cloudflare.headers import HEADERS

def post_file_sync(url, body, headers=HEADERS, name=''):
  res = post_request(url, data=body, headers=headers)
  if res.status_code == 200:
    info(f'[🔥]: {res.status_code} {name}')
    val = res.json()
    return val['result']['id']
  else: 
    info(f'[🔥❌]: {type} https://http.cat/{res.status_code}')
    return None