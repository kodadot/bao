def save_file(file_name, data, path='./'):
  with open(path + file_name, 'wb') as outfile:
    outfile.write(data)

def read_file(file_name, path='./'):
  with open(path + file_name, 'rb') as infile:
    return infile.read()