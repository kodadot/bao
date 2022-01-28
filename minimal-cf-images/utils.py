from constants import FULL_IPFS_PREFIX, IPFS_PREFIX, PINATA_BASE_API


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