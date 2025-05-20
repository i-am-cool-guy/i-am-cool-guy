from telethon import events
from telethon.tl.types import MessageEntityMention, MessageEntityMentionName, UserStatusOffline, UserStatusOnline
from telethon.tl.functions.users import GetFullUserRequest
from userbot import Neo, PREFIX
from userbot.utils import lang
import os
import mimetypes

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
      username = event.message.raw_text[ent.offset : ent.offset + ent.length]
      user = await Neo.get_entity(username)
      user_id = user.id
  full = await Neo(GetFullUserRequest(user_id))
  user = full.users[0]
  extra = full.full_user
  pp_path = os.path.join("../temp/", f"{user_id}")
  downloaded = await Neo.download_profile_photo(user_id, file=pp_path)
  if downloaded:
    mime_type, _ = mimetypes.guess_type(downloaded)
    is_image = mime_type is not None and mime_type.startswith('image/')
  else:
    is_image = False
  status = 'Unknown'
  if isinstance(user.status, UserStatusOnline):
    status = 'Online'
  elif isinstance(user.status, UserStatusOffline):
    status = f"Last seen: {user.status.was_online.strftime('%Y-%m-%d %H:%M:%S')}"
  info = (
    f"User ID: {user.id}\n"
    f"Username: @{user.username or '—'}\n"
    f"First Name: {user.first_name or '—'}\n"
    f"Last Name: {user.last_name or '—'}\n"
    f"Phone: {user.phone or 'Hidden'}\n"
    f"Bio: {extra.about or '—'}\n"
    f"Status: {status}\n"
    f"Common Chats: {extra.common_chats_count}\n"
    f"Blocked: {'Yes' if extra.blocked else 'No'}\n"
    f"Premium User: {'Yes' if user.premium else 'No'}\n"
    f"Is Bot: {'Yes' if user.bot else 'No'}\n"
  )
  if downloaded:
    if not is_image:
      await Neo.send_file(event.chat_id, downloaded, caption=info, force_document=True)
    else:
      await Neo.send_file(event.chat_id, downloaded, caption=info)
  else:
    await event.reply(info)
