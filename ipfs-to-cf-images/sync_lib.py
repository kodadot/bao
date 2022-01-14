from requests import get, post
from logging import info

from headers import CF_IMAGES_URI, HEADERS

def post_to_cf(name, content, type):
  files = {'file': (name, content, type)}
  res = post(CF_IMAGES_URI, files=files, headers=HEADERS)
  info(f'[🔥]: {res.status_code}')
  if res.status_code == 200:
    val = res.json()
    return val['result']['id']
  else: 
    info(f'[🔥❌]: {name}, {type} https://http.cat/{res.status_code}')
    return None


def fetch_all(meta):
  final = []
  for item in meta:
    info(f'[ALL]: Processing {item["id"]}')
    name, value, type = fetch_one(item)
    cloudflare_image_uuuid = post_to_cf(name, value, type)
    if cloudflare_image_uuuid is not None:
      final.append((item['id'], cloudflare_image_uuuid))
  return final



def fetch_one(item):
  res = get(item['value'])
  type = res.headers['Content-Type']
  suffix = type.split('/')[1]
  name = item['id'] + '.' + suffix
  with open('res/' + name, 'wb') as f:
    f.write(res.content)
  return (name, res.content, type)
  