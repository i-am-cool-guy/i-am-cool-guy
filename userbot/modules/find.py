from telethon import events
from userbot import Neo, PREFIX
from userbot.utils import lang
LANG = lang('whois')

@Neo.command(
  pattern='^whois ?(.*)',
  info='Get information of the user.'
)
async def whois(event):
  info = ''
