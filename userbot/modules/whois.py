from telethon import events
from telethon.tl.types import MessageEntityMention, MessageEntityMentionName
from userbot import Neo, PREFIX
from userbot.utils import lang
import os

LANG = lang('whois')

@Neo.command(
  pattern='^whois ?(.*)',
  info='Get information of the user.'
)
async def whois(event):
  user_id = (await Neo.get_me()).id
  if event.is_reply:
    replied_msg = await event.get_reply_message()
    sender = await replied_msg.get_sender()
    user_id = sender.id
  for ent in event.message.entities or []:
    if isinstance(ent, MessageEntityMentionName):
      user_id = ent.user_id
    elif isinstance(ent, MessageEntityMention):
      username = event.message.raw_text[ent.offset:ent.offset+ent.length]
      user = await Neo.get_entity(username)
      user_id = user.id
  user_info = await Neo.get_entity(user_id)
  pp = await Neo.download_profile_photo(user_id, file=os.path.join("../temp/", f"{user_id}.jpg"))
  info = f"User ID: {user_info.id}\nUsername: {user_info.username}\nFirst Name: {user_info.first_name}"
  if user_info.last_name:
    info += f"\nLast Name: {user_info.last_name}"
  info += f"\nIs Bot: {'Yes' if user_info.bot else 'No'}"
  if pp:
    await Neo.send_file(event.chat_id, f"../temp/{user_id}.jpg", caption=info)
  else:
    await event.reply(info)
