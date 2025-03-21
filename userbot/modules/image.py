from telethon import events 
from google_images_search import GoogleImagesSearch
from userbot import Neo
from userbot.utils import lang
import os
LANG = lang('image')

@Neo.command(
  pattern='^image ?(.*)',
  info='Download google images for your query.'
)
async def image(event):
  text = event.pattern_match.group(1) or False
  if text == False:
    return await event.reply('**Please enter some keywords to search!**')
  gis.search({
    "q": text,
    "num": 10,
    "safe": "on",
    "fileType": "jpg",
    "imgType": "photo",
    "searchType": "image"
  })
  for image in gis.results():
    image.download('/path/to/download/folder')
  
