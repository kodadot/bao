def fast_extract(ipfs):
  if not ipfs:
    return ''
  return ipfs.replace('ipfs://ipfs/', '')