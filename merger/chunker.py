from os import getenv, getcwd
from sys import argv, path
path.append(getcwd())
from json import dump, load
from cloudflare.chunk import chunkify


def to_chunks():
  with open('merge.json') as meta_file:
    processed = load(meta_file)
    all = list(chunkify(processed, 1000))
    for index, chunk in enumerate(all):
      with open(f'meta/chunk{index}.json', 'w') as f:
        dump(chunk, f, indent=2)
    return len(all)

def to_output_chunks():
  with open('merger/output.txt', 'r') as meta_file:
    processed = meta_file.readlines()
    all = list(chunkify(processed, 1000))
    for index, chunk in enumerate(all):
      with open(f'merger/chunk/chunk{index}.txt', 'w') as f:
        # save the list to file
        f.writelines(chunk)
    return len(all)

if __name__ == '__main__':
  # print(to_chunks())
  print(to_output_chunks())