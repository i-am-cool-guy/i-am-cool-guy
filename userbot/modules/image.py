from telethon import events 
from google_images_downloader import GoogleImagesDownloader
downloader.download("bear")  # Download 50 images in ./downloads folder

downloader.download("cat", destination="C:\download\destination")  # Download at specified destination
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
  downloader = GoogleImagesDownloader(browser="chrome", show=False, debug=False,
                                    quiet=False, disable_safeui=False)
  downloader.download(text, limit=10, destination="../temp/", file_format="jpg")
  downloader.close()
