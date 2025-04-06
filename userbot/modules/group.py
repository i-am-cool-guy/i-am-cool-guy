from userbot import Neo
from userbot.utils import lang
from telethon.tl.functions.channels import EditBannedRequest, EditAdminRequest, InviteToChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest, EditChatDefaultBannedRightsRequest
from telethon.tl.types import ChatBannedRights, ChatAdminRights
from datetime import timedelta, datetime

LANG = lang('group')

def parse_duration(duration_str):
  pattern = r'(?:(\d+)d)?\s*(?:(\d+)h)?\s*(?:(\d+)m)?\s*(?:(\d+)s)?'
  match = re.match(pattern, duration_str)
  if not match:
    return None
  days, hours, minutes, seconds = (int(match.group(i) or 0) for i in range(1, 5))
  return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds).total_seconds()

@Neo.command(
  pattern='^mute ?(\S+)?(?:\s+(.+))?',
  info=LANG['MUTE_INFO'],
  usage='.mute <user> <time>',
  example='.mute @username 10m'
)
async def mute(event):
  user = await event.get_chat() if event.is_reply else event.pattern_match.group(1)
  duration_str = event.pattern_match.group(2) or None
  if not user:
    return await event.edit(LANG['NO_USER'])
  
  until_date = None
  if duration_str:
    duration_seconds = parse_duration(duration_str)
    if duration_seconds is None:
      return await event.edit(LANG['INVALID_TIME'])
    until_date = datetime.now().timestamp() + duration_seconds
    
  rights = ChatBannedRights(until_date=until_date, send_messages=True)
  await event.client(EditBannedRequest(event.chat_id, user, rights))
  await event.edit(LANG['MUTED'].format(user, duration_str if duration_str else 'forever'))

@Neo.command(
  pattern='^unmute ?(\S+)?(?:\s+(.+))?',
  info=LANG['UNMUTE_INFO'],
  usage='.unmute <user> <time>',
  example='.unmute @username 10m'
)
async def unmute(event):
  user = await event.get_chat() if event.is_reply else event.pattern_match.group(1)
  duration_str = event.pattern_match.group(2) or None
  if not user:
    return await event.edit(LANG['NO_USER'])
  
  until_date = None
  if duration_str:
    duration_seconds = parse_duration(duration_str)
    if duration_seconds is None:
      return await event.edit(LANG['INVALID_TIME'])
    until_date = datetime.now().timestamp() + duration_seconds
    
  rights = ChatBannedRights(until_date=until_date, send_messages=False)
  await event.client(EditBannedRequest(event.chat_id, user, rights))
  await event.edit(LANG['UNMUTED'].format(user))

@Neo.command(
  pattern='^ban ?(.*)',
  info=LANG['BAN_INFO'],
  usage='.ban <user>',
  example='.ban @username'
)
async def ban(event):
  user = await event.get_chat() if event.is_reply else event.pattern_match.group(1)
  duration_str = event.pattern_match.group(2) or None
  if not user:
    return await event.edit(LANG['NO_USER'])
  
  until_date = None
  if duration_str:
    duration_seconds = parse_duration(duration_str)
    if duration_seconds is None:
      return await event.edit(LANG['INVALID_TIME'])
    until_date = datetime.now().timestamp() + duration_seconds
    
  rights = ChatBannedRights(until_date=until_date, view_messages=True)
  await event.client(EditBannedRequest(event.chat_id, user, rights))
  await event.edit(LANG['BANNED'].format(user))

@Neo.command(
    pattern='^kick ?(.*)',
    info=LANG['KICK_INFO'],
    usage='.kick <user>',
    example='.kick @username'
)
async def kick(event):
  user = await event.get_chat() if event.is_reply else event.pattern_match.group(1)
  if not user:
    return await event.edit(LANG['NO_USER'])
  await event.client(EditBannedRequest(event.chat_id, user, ChatBannedRights(until_date=None, view_messages=True)))
  await event.client(EditBannedRequest(event.chat_id, user, ChatBannedRights(until_date=None, view_messages=False)))
  return await event.edit(LANG['KICKED'].format(user))

@Neo.command(
  pattern='^add ?(.*)',
  info=LANG['ADD_INFO'],
  usage='.add <user>',
  example='.add @username'
)
async def add(event):
  user = event.pattern_match.group(1)
  if not user:
    return await event.edit(LANG['NO_USER'])
  await event.client(InviteToChannelRequest(event.chat_id, [user]))
  await event.edit(LANG['ADDED'].format(user))

@Neo.command(
  pattern=r'^promote ?(.*)',
  info=LANG['PROMOTE_INFO'],
  usage='.promote <user>',
  example='.promote @username'
)
async def promote(event):
  user = await event.get_chat() if event.is_reply else event.pattern_match.group(1)
  if not user:
    return await event.edit(LANG['NO_USER'])
  rights = ChatAdminRights(
    change_info=True,
    post_messages=True,
    edit_messages=True,
    delete_messages=True,
    ban_users=True,
    invite_users=True,
    pin_messages=True,
    add_admins=False,
    anonymous=False,
    manage_call=True
  )
  await event.client(EditAdminRequest(event.chat_id, user, rights, "Admin"))
  await event.edit(LANG['PROMOTED'].format(user))

@Neo.command(
  pattern=r'^demote ?(.*)',
  info=LANG['DEMOTE_INFO'],
  usage='.demote <user>',
  example='.demote @username'
)
async def demote(event):
  user = await event.get_chat() if event.is_reply else event.pattern_match.group(1)
  if not user:
    return await event.edit(LANG['NO_USER'])
  rights = ChatAdminRights(
    change_info=False,
    post_messages=False,
    edit_messages=False,
    delete_messages=False,
    ban_users=False,
    invite_users=False,
    pin_messages=False,
    add_admins=False,
    anonymous=False,
    manage_call=False
  )
  await event.client(EditAdminRequest(event.chat_id, user, rights, "Admin"))
  await event.edit(LANG['DEMOTED'].format(user))

@Neo.command(
  pattern='^pin$',
  info=LANG['PIN_INFO'],
  usage='.pin',
  example='.pin'
)
async def pin(event):
  if not event.reply_to_msg_id:
    return await event.edit(LANG['NO_MSG'])
  await event.client.pin_message(event.chat_id, event.reply_to_msg_id)
  await event.edit(LANG['PINNED'])

@Neo.command(
  pattern='^revoke$',
  info=LANG['REVOKE_INFO'],
  usage='.revoke',
  example='.revoke'
)
async def revoke(event):
  link = await event.client(ExportChatInviteRequest(event.chat_id))
  await event.edit(LANG['REVOKED'].format(link))

@Neo.command(
  pattern='^link$',
  info=LANG['LINK_INFO'],
  usage='.link',
  example='.link'
)
async def link(event):
  link = await event.client(ExportChatInviteRequest(event.chat_id))
  await event.edit(LANG['LINK'].format(link))

@Neo.command(
  pattern='^open$',
  info=LANG['OPEN_INFO'],
  usage='.open',
  example='.open'
)
async def open_chat(event):
  await event.client(EditChatDefaultBannedRightsRequest(
    peer=event.chat_id,
    banned_rights=ChatBannedRights(send_messages=False, until_date=None)
  ))
  await event.edit(LANG['OPENED'])

@Neo.command(
  pattern='^close$',
  info=LANG['CLOSE_INFO'],
  usage='.close',
  example='.close'
)
async def close_chat(event):
  await event.client(EditChatDefaultBannedRightsRequest(
    peer=event.chat_id,
    banned_rights=ChatBannedRights(send_messages=True, until_date=None)
  ))
  await event.edit(LANG['CLOSED'])
