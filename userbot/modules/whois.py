from telethon import events
from telethon.tl.types import MessageEntityMentionName
from userbot import Neo, PREFIX
from userbot.utils import lang
import os
LANG = lang('whois')

@Neo.command(
  pattern='^whois ?(.*)',
  info='Get information of the user.'
)
async def whois(event):
  user = (await Neo.get_me()).id
  if event.is_reply:
    replied_msg = await event.get_reply_message()
    user = (await replied_msg.get_sender()).id
  if event.entities:
    for entity in event.entities:
      if isinstance(entity, MessageEntityMentionName):
        user = entity.user_id
  user_info = await Neo.get_entity(user)
  print(user_info)
  pp = await Neo.download_profile_photo(user, file=os.path.join("../temp/", f"{user}.jpg"))
  info = f"User ID: {user_info.id}\nUsername: {user_info.username}\nFirst Name: {user_info.first_name}{f'\nLast Name: {user_info.last_name}' if user_info.last_name else '\n'}Is Bot: {'Yes' if user_info.bot else 'No'}"
  if pp:
    await Neo.send_file(event.chat_id, f"../temp/{user}.jpg", caption=info)
  else:
    await event.reply(info)
