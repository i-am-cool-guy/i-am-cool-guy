from telethon import events 
from google_images_downloader import GoogleImagesDownloader
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
  images = []
  for image in os.listdir("../temp/"):
    if image.endsWith("jpg") or image.endsWith("png") or image.endsWith("jpeg"):
      images.append(os.path.join("../temp/", image)
  if not images:
    return await event.reply('**No images found.**')
  for path in images:
    await Neo.send_file(event.chat_id, path)
    os.remove(image_path)
