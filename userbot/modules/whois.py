import os

from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
from userbot import Neo
from userbot.utils import lang

LANG = lang("whois")
""""
@Neo.command(
  pattern="^whois ?(.*)",
  info="Get user details.",
  usage=".whois <reply/mention/id>",
  example=".whois @telegram"
)
async def whois(event):
  text = event.pattern_match.group(1)
  if text and isinstance(text, int):
    user = int(event.pattern_match.group(1))
  elif
    (str((await event.get_reply_message()).from_id) if event.reply_to_msg_id else None) or
    (str(event.message.entities[0].user_id) if event.message.entities and isinstance(event.message.entities[0], MessageEntityMentionName) else None) or
    (await Neo.get_me()).id
  )
  user = int(user) if user.isnumeric() else user
  user_obj = await Neo.get_entity(user)
  userinfo = await Neo(GetFullUserRequest(user_obj.id))
"""
