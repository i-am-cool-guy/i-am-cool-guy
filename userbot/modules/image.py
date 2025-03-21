from telethon import events 
from google_images_download import google_images_download
from userbot import Neo
from userbot.utils import lang
import os
LANG = lang('image')

@Neo.command(
  pattern='^image ?(.*)',
  info='Download google images for your query.'
)
async def image(event):
  if event.pattern_match.group(1):
    response = google_images_download.googleimagesdownload()
    images = response.download({ "keywords": f"{event.pattern_match.group(1)} -sa", "limit": 10 }) 
    print(images)
  else:
    await event.reply("Cannot find images for your query!")
