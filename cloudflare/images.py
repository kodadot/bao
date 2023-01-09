from aiohttp import FormData
from cloudflare.headers import CF_IMAGES_URI, HEADERS
from cloudflare.rest import post_file_async

async def send_to_cf_images(form, name):
  res = await post_file_async(CF_IMAGES_URI, form, headers=HEADERS, name=name)
  return res

async def upload_image_via_url(url, name):
  form = FormData()
  form.add_field("url", url)
  form.add_field("id", name)
  return await send_to_cf_images(form, name)

async def upload_image_via_file(content, name, type):
  form = FormData()
  form.add_field("file", content, filename=name, content_type=type)
  form.add_field("id", name)
  return await send_to_cf_images(form, name)
