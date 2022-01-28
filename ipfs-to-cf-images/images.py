from PIL import Image

size = 666, 666
# If you 100% trust your inputs, you can also disable the check completely with
Image.MAX_IMAGE_PIXELS = None


def resize_image(image, path='opt/'):
    img = Image.open(image)
    img.thumbnail(size, Image.ANTIALIAS)
    img.save(path + image)

def wib():
  with open('res.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
      p = line.strip().replace('./', 'opt/res/')
      resize_image(p)
