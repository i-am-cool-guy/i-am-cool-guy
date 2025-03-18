from telethon import events
from userbot import Neo, PREFIX
from userbot.utils import lang
LANG = lang('whois')

@Neo.command(
  pattern='^whois ?(.*)',
  info='Get information of the user.'
)
async def whois(event):
  user = Neo.me.id
  if event.is_reply:
    replied_msg = await event.get_reply_message()
    user = await replied_msg.get_sender()
