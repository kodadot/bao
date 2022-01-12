from json import load
from requests import get, post
from dotenv import load_dotenv
from os import getenv
from logging import info, basicConfig, INFO
from signal import signal, SIGINT

from utils import only_with_value, map_to_kv

load_dotenv()

ACCOUNT = getenv('ACCOUNT')
API_KEY = getenv('API_KEY')

CF_IMAGES_URI = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/images/v1"
HEADERS={"Authorization": f"Bearer {API_KEY}"}
CF_DURABLE_OBJECT = "https://durable-jpeg.kodadot.workers.dev"

def handle_sigint(signal_received, frame):
  print('\n\nSIGINT or CTRL-C detected. Exiting gracefully')
  exit(1)

signal(SIGINT, handle_sigint)

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
  

def init():
  for i in range(0, 2):
    with open(f'meta/chunk{i}.json') as f:
      info(f'[CHUNK]: Running chunk {i}')
      meta = load(f)
      final = fetch_all(meta)
      store_to_durable_object(final)
      info(f'[CHUNK]: OK {i}')

def full_init():
  with open('meta.json') as meta_file:
      meta = load(meta_file)
      unwrapped = meta['data']['meta']
      processed = list(filter(only_with_value, map(map_to_kv, unwrapped)))
      all = fetch_all(processed)
      info(f'[DONE]: Processing {len(all)} items')
      return post_to_cf(all)

if __name__ == '__main__':
  basicConfig(format='%(levelname)s: %(message)s', level=INFO)
  info('[APP]: Running')
  init()