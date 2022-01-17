from cmath import inf
from operator import le
from requests import get as get_sync, post as post_sync
from logging import info

CF_DURABLE_OBJECT = "https://durable-jpeg.kodadot.workers.dev"


def get_kv_list(keys):
  res = get_sync(CF_DURABLE_OBJECT + '/batch', json={'keys': keys})
  return res.json()


def store_to_durable_object(kv_list):
  keys = dict(kv_list)
  info(f'[🔥]: Storing {len(kv_list)} keys')
  res = post_sync(CF_DURABLE_OBJECT + '/write', json=keys)
  info(f'[OBJECT]: ❄️ {res.status_code}')