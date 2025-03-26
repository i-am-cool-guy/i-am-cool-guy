from telethon import events 
from userbot import Neo
from userbot.utils import lang, request
import os

LANG = lang('weather')

@Neo.command(
    pattern='^weather ?(.*)',
    info='Get weather of a specific place.'
)
async def weather(event):
    text = event.pattern_match.group(1) or False
    if not text:
        return await event.reply('**Please enter any place name!**')
    json = await request('GET', f"http://api.openweathermap.org/data/2.5/weather?q={text}&units=metric&appid=060a6bcfa19809c2cd4d97a212b19273&language=en")
    
