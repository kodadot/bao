from json import load
from requests import get, post
from dotenv import load_dotenv
from os import getenv
from logging import info, basicConfig, INFO

load_dotenv()

PINATA_BASE_API = "https://kodadot.mypinata.cloud/"
IPFS_PREFIX = "ipfs://"
FULL_IPFS_PREFIX = "ipfs://ipfs/"
CF_IMAGES_URI = "https://api.cloudflare.com/client/v4/accounts/b3f9fdfd827152316d080a5ddee59915/images/v1"
HEADERS={"Authorization": f"Bearer {getenv('API_KEY')}"}
CF_DURABLE_OBJECT = "https://durable-jpeg.kodadot.workers.dev"

def map_to_kv(meta):
  return {
    'id': meta['id'].replace(FULL_IPFS_PREFIX, ""),
    'value': unwrap_or_default(meta['image'], '').replace(IPFS_PREFIX, PINATA_BASE_API),
  }

def unwrap_or_default(value, default):
  if value is None:
    return default
  return value

def only_with_value(meta):
  return meta['value'] != ''

def post_to_cf(name, content, type):
  files = {'file': (name, content, type)}
  res = post(CF_IMAGES_URI, files=files, headers=HEADERS)
  val = res.json()
  return val['result']['id']

def store_to_durable_object(kv_list):
  keys = dict(kv_list)
  res = post(CF_DURABLE_OBJECT + '/write', json=keys)
  print(res.status_code)
  


def fetch_all(meta):
  final = []
  for item in meta:
    info(f'[ALL]: Processing {item["id"]}')
    name, value, type = fetch_one(item)
    cloudflare_image_uuuid = post_to_cf(name, value, type)
    final.append((cloudflare_image_uuuid, item['id']))
  return final



def fetch_one(item):
  res = get(item['value'])
  type = res.headers['Content-Type']
  suffix = type.split('/')[1]
  name = item['id'] + '.' + suffix
  with open('res/' + name, 'wb') as f:
    f.write(res.content)
  return (name, res.content, type)
  

def init():
  basicConfig(format='%(levelname)s: %(message)s', level=INFO)
  info('[APP]: Running')
  with open('meta.json') as meta_file:
      meta = load(meta_file)
      unwrapped = meta['data']['meta']
      processed = list(filter(only_with_value, map(map_to_kv, unwrapped)))
      all = fetch_all(processed)
      info(f'[DONE]: Processing {len(all)} items')
      return post_to_cf(all)

if __name__ == '__main__':
  init()