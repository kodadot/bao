def chunkify(metadata, size):
    """
    Split a list into chunks of a specified size.
    """
    for i in range(0, len(metadata), size):
        yield metadata[i:i + size]
