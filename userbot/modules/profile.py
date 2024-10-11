from userbot import Neo
from userbot.utils import lang
from telethon.errors.rpcerrorlist import PhotoExtInvalidError, UsernameOccupiedError
from telethon.tl.functions.account import UpdateProfileRequest, UpdateUsernameRequest
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest
from telethon.tl.types import User, Chat, Channel
import os
LANG = lang('profile')

@Neo.command(
  pattern="^reserved$",
  info=LANG['RESERVED_INFO']
)
async def reserved(event):
  result = await Neo(GetAdminedPublicChannelsRequest())
  if len(result.chats) == 0:
    return await event.edit(LANG['NO_RESERVED'])
  res = ''
  for chat in result.chats:
    res += f"__{LANG['TITLE']}:__ **{chat.title}**\n__{LANG['USERNAME']}:__ **@{chat.username}**\n__{LANG['CREATED_DATE']}:__ **{chat.date.strftime('%d-%m-%y')}**\n__{LANG['CREATED_TIME']}:__ **{chat.date.strftime('%H:%M:%S')}**\n\n"
  return await event.edit(res)

@Neo.command(
  pattern="^name ?(.*)",
  info=LANG['NAME_INFO'],
  usage='.name <first_name last_name>',
  example='.name Neo userbot'
)
async def name(event):
  text = first = event.pattern_match.group(1) or None
  last = ""
  if text == None:
    return event.edit(LANG['NAME_NONE'])
  if " " in text:
    first, last = text.split(" ")

  await Neo(UpdateProfileRequest(first_name=first, last_name=last))
  return await event.edit(LANG['SUC_NAME'].format(text))

@Neo.command(
  pattern="^bio ?(.*)",
  info=LANG['BIO_INFO'],
  usage='.bio <text>',
  example='.bio Neo - telegram userbot'
)
async def bio(event):
  reply_message = await event.get_reply_message()
  text = event.pattern_match.group(1) or (reply_message.text if reply_message else None)
  if text == None:
    return await event.edit(LANG['BIO_NONE'])
  bio = text.strip()
  await Neo(UpdateProfileRequest(about=bio))
  return await event.edit(LANG['SUC_BIO'].format(bio))
