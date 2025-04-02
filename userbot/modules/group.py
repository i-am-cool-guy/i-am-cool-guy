from userbot import Neo
from userbot.utils import lang
from telethon.tl.functions.channels import EditBannedRequest, EditAdminRequest, InviteToChannelRequest, ExportChatInviteRequest
from telethon.tl.types import ChatBannedRights, ChatAdminRights
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsAdmins
from datetime import timedelta
import re

LANG = lang('group')

def parse_time(time_str):
  match = re.match(r"(\d+)([smhd])", time_str)
  if match:
    value, unit = int(match[1]), match[2]
    if unit == "s":
      return timedelta(seconds=value)
    elif unit == "m":
      return timedelta(minutes=value)
    elif unit == "h":
      return timedelta(hours=value)
    elif unit == "d":
      return timedelta(days=value)
  return None

async def is_admin(event):
  user = await event.client.get_me()
  admins = await event.client(GetParticipantsRequest(event.chat_id, ChannelParticipantsAdmins()))
  if user.id not in [admin.id for admin in admins.participants]:
    await event.edit(LANG['NOT_ADMIN'])
    return False
  return True

async def get_user(event):
  if event.is_reply:
    return (await event.get_reply_message()).sender_id
  user = event.pattern_match.group(1)
  return await Neo.get_entity(user) if user else None

@Neo.command(
  pattern='^restrict ?(.*)',
  info=LANG['RESTRICT_INFO'],
  usage='.restrict <type>',
  example='.restrict poll'
)
async def restrict(event):
  if not await is_admin(event):
    return
  restriction = event.pattern_match.group(1)
  if not restriction:
    return await event.edit(LANG['NO_TYPE'])
  
  rights = ChatBannedRights(**{restriction: True})
  await Neo(EditBannedRequest(event.chat_id, None, rights))
  await event.edit(LANG['RESTRICTED'].format(restriction))

@Neo.command(
  pattern='^unrestrict ?(.*)',
  info=LANG['UNRESTRICT_INFO'],
  usage='.unrestrict <type>',
  example='.unrestrict poll'
)
async def unrestrict(event):
  if not await is_admin(event):
    return
  restriction = event.pattern_match.group(1)
  if not restriction:
    return await event.edit(LANG['NO_TYPE'])
  
  rights = ChatBannedRights(**{restriction: False})
  await Neo(EditBannedRequest(event.chat_id, None, rights))
  await event.edit(LANG['UNRESTRICTED'].format(restriction))
