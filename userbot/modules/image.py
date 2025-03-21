from telethon import events 
from simple_image_download import simple_image_download as sid
from userbot import Neo
from userbot.utils import lang
import os

LANG = lang('image')

@Neo.command(
    pattern='^image ?(.*)',
    info='Download Google images for your query.'
)
async def image(event):
    text = event.pattern_match.group(1) or False
    if text == False:
        return await event.reply('**Please enter some keywords to search!**')
    downloader = sid.simple_image_download()
    download_path = "../temp/"
    downloader.download(text, limit=10, extensions={".jpg", ".png", ".jpeg"}, output_directory=download_path)
    images = []
    for image in os.listdir(download_path):
        if image.endswith(("jpg", "png", "jpeg")):
            images.append(os.path.join(download_path, image))
    if not images:
        return await event.reply('**No images found.**')
    for image_path in images:
        await Neo.send_file(event.chat_id, image_path)
        os.remove(image_path)
