from userbot import Neo
from userbot.utils import lang
from telethon.errors import ImageProcessFailedError, PhotoCropSizeSmallError
from telethon.errors.rpcerrorlist import PhotoExtInvalidError, UsernameOccupiedError
from telethon.tl.functions.account import UpdateProfileRequest, UpdateUsernameRequest
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest
from telethon.tl.functions.photos import DeletePhotosRequest, GetUserPhotosRequest, UploadProfilePhotoRequest
from telethon.tl.types import InputPhoto, MessageMediaPhoto, User, Chat, Channel
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

@Neo.command(
  pattern="^pp ?(.*)",
  info=LANG['PP_INFO']
)
async def pp(event):
  replied = await event.get_reply_message()
  if replied.media:
    if isinstance(replied.media, MessageMediaPhoto):
      image = await Neo.download_media(message=replied.photo)
    elif 'image' in replied.media.document.mime_type.split('/'):
      image = await Neo.download_file(replied.media.document)
    else:
      return await event.edit(LANG['PP_NONE'])

    try:
      image_file = await Neo.upload_file(image)
      await Neo(UploadProfilePhotoRequest(image_file))
      os.remove(image)
      return await event.edit(LANG['SUC_PP'])
    except PhotoCropSizeSmallError:
      return await event.edit(LANG['PP_SMALL'])
    except ImageProcessFailedError:
      return await event.edit(LANG['PP_FAILED'])
    except PhotoExtInvalidError:
      return await event.edit(LANG['PP_NONE'])
