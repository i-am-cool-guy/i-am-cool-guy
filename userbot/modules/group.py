from userbot import Neo
from userbot.utils import lang
from telethon.tl.functions.channels import EditBannedRequest, EditAdminRequest, InviteToChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
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
  pattern='^mute ?(.*)',
  info=LANG['MUTE_INFO'],
  usage='.mute <user> <duration>',
  example='.mute @username 10m'
)
async def mute(event):
  if not await is_admin(event):
    return
  user = await get_user(event)
  if not user:
    return await event.edit(LANG['NO_USER'])
  duration = parse_time(event.pattern_match.group(2))
  rights = ChatBannedRights(until_date=duration, send_messages=True)
  await Neo(EditBannedRequest(event.chat_id, user, rights))
  await event.edit(LANG['MUTED'].format(user))

@Neo.command(
  pattern='^unmute ?(.*)',
  info=LANG['UNMUTE_INFO'],
  usage='.unmute <user>',
  example='.unmute @username'
)
async def unmute(event):
  if not await is_admin(event):
    return
  user = await get_user(event)
  if not user:
    return await event.edit(LANG['NO_USER'])
  rights = ChatBannedRights(send_messages=False)
  await Neo(EditBannedRequest(event.chat_id, user, rights))
  await event.edit(LANG['UNMUTED'].format(user))

@Neo.command(
  pattern='^ban ?(.*)',
  info=LANG['BAN_INFO'],
  usage='.ban <user>',
  example='.ban @username'
)
async def ban(event):
  if not await is_admin(event):
    return
  user = await get_user(event)
  if not user:
    return await event.edit(LANG['NO_USER'])
  rights = ChatBannedRights(until_date=None, view_messages=True)
  await Neo(EditBannedRequest(event.chat_id, user, rights))
  await event.edit(LANG['BANNED'].format(user))

@Neo.command(
  pattern='^kick ?(.*)',
  info=LANG['KICK_INFO'],
  usage='.kick <user>',
  example='.kick @username'
)
async def kick(event):
  if not await is_admin(event):
    return
  user = await get_user(event)
  if not user:
    return await event.edit(LANG['NO_USER'])
  rights = ChatBannedRights(until_date=None, view_messages=True)
  await Neo(EditBannedRequest(event.chat_id, user, rights))
  await Neo(EditBannedRequest(event.chat_id, user, ChatBannedRights(view_messages=False)))
  await event.edit(LANG['KICKED'].format(user))

@Neo.command(
  pattern='^add ?(.*)',
  info=LANG['ADD_INFO'],
  usage='.add <user>',
  example='.add @username'
)
async def add(event):
  if not await is_admin(event):
    return
  user = event.pattern_match.group(1)
  if not user:
    return await event.edit(LANG['NO_USER'])
  await Neo(InviteToChannelRequest(event.chat_id, [user]))
  await event.edit(LANG['ADDED'].format(user))

@Neo.command(
  pattern='^promote ?(.*)',
  info=LANG['PROMOTE_INFO'],
  usage='.promote <user> <permissions>',
  example='.promote @username pin_messages'
)
async def promote(event):
  if not await is_admin(event):
    return
  user = await get_user(event)
  if not user:
    return await event.edit(LANG['NO_USER'])
  permissions = event.pattern_match.group(2)
  rights = ChatAdminRights(**{permissions: True}) if permissions else ChatAdminRights(post_messages=True, add_admins=False, pin_messages=True)
  await Neo(EditAdminRequest(event.chat_id, user, rights, LANG['PROMOTED']))
  await event.edit(LANG['PROMOTED'].format(user))

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
