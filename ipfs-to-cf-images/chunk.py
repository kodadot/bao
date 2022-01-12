from utils import only_with_value, map_to_kv
from json import dump, load

def chunkify(metadata, size):
    """
    Split a list into chunks of a specified size.
    """
    for i in range(0, len(metadata), size):
        yield metadata[i:i + size]


def wib():
  with open('meta.json') as meta_file:
    meta = load(meta_file)
    unwrapped = meta['data']['meta']
    processed = list(filter(only_with_value, map(map_to_kv, unwrapped)))
    processed.reverse()
    all = list(chunkify(processed, 20))
    for index, chunk in enumerate(all):
      with open(f'meta/chunk{index}.json', 'w') as f:
        dump(chunk, f)
    return len(all)