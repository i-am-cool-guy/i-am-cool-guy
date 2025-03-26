from telethon import events 
from userbot import Neo
from userbot.utils import lang
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
