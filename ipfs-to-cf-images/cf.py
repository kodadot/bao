from logging import INFO, basicConfig, info
from requests import get as get_sync
from headers import CF_IMAGES_URI, HEADERS
from itertools import chain
from dog import store_to_durable_object
from utils import map_kb_to_tuple


def get_all_stored_images():
  for i in range(1, 505):
    params = { 'page': i, 'per_page': 100 }
    res = get_sync(CF_IMAGES_URI, headers=HEADERS, params=params)
    print(f'[🏞]: Page {i} has status {res.status_code}')
    if res.status_code == 200:
      val = res.json()['result']['images']
      if len(val) == 0:
        print(f'[🌎]: Page {i} is empty ending')
        break
      final = map(map_kb_to_tuple, map(map_to_kv, val))
      store_to_durable_object(list(final))


def map_to_kv(item):
  id = item['filename'].split('.')[0]
  return { 'key': id, 'value': item['id'] }

if __name__ == '__main__':
  basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=INFO, datefmt='%H:%M:%S')
  info('[🌎]: Running')
  get_all_stored_images()