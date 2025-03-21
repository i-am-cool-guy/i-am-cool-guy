from telethon import events 
from simple_image_download.simple_image_download import simple_image_download
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
    if not text:
        return await event.reply('**Please enter some keywords to search!**')
    downloader = simple_image_download()
    download_path = "../temp/"
    downloader.download(text, limit=10)
    image_folder = os.path.join("simple_images", text)
    if not os.path.exists(image_folder):
        return await event.reply('**No images found.**')
    images = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(("jpg", "png", "jpeg"))]
    if not images:
        return await event.reply('**No images found.**')
    for image_path in images:
        await Neo.send_file(event.chat_id, image_path)
        os.remove(image_path)
