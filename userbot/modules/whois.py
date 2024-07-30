import os

from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
from userbot import Neo
from userbot.utils import lang

LANG = lang("whois")

@Neo.command(
  pattern="^whois ?(.*)",
  info="Get user details.",
  usage=".whois <reply/mention/id>",
  example=".whois @telegram"
)
async def whois(event):
  text = event.pattern_match.group(1)
  reply = await event.get_reply_message()
  user = ""
  if text and isinstance(text, int):
    user = int(event.pattern_match.group(1))
  elif reply:
    user = reply.from_id
  elif event.message.entities and isinstance(event.message.entities[0], MessageEntityMentionName):
    user = event.message.entities[0].user_id

  user = await Neo.get_entity(user)
  info = await Neo(GetFullUserRequest(user.id))
