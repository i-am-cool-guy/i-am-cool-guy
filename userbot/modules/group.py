import re
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
  return timedelta(days=days, hours=hours, minutes=seconds).total_seconds()

@Neo.command(
  pattern='^mute ?(\S+)?(?:\s+(.+))?',
  info=LANG['MUTE_INFO'],
  usage='.mute <user> <time>',
  example='.mute @username 10m'
)
async def mute(event):
  user = await event.get_input_sender() if event.is_reply else event.pattern_match.group(1)
  duration_str = event.pattern_match.group(2)
  if not user:
    return await event.edit(LANG['NO_USER'])
  entity = await event.client.get_entity(user)
  duration_seconds = parse_duration(duration_str) if duration_str else None
  until_date = datetime.utcnow() + timedelta(seconds=duration_seconds) if duration_seconds else None
  rights = ChatBannedRights(until_date=until_date, send_messages=True)
  current_rights = (await event.client.get_permissions(event.chat_id, entity)).send_messages
  if current_rights is False:
    return await event.edit(LANG['ALREADY_MUTED'])
  await event.client(EditBannedRequest(event.chat_id, entity, rights))
  await event.edit(LANG['MUTED'].format(entity.id, duration_str if duration_str else 'forever'))

@Neo.command(
  pattern='^unmute ?(\S+)?(?:\s+(.+))?',
  info=LANG['UNMUTE_INFO'],
  usage='.unmute <user> <time>',
  example='.unmute @username 10m'
)
async def unmute(event):
  user = await event.get_input_sender() if event.is_reply else event.pattern_match.group(1)
  duration_str = event.pattern_match.group(2)
  if not user:
    return await event.edit(LANG['NO_USER'])
  entity = await event.client.get_entity(user)
  duration_seconds = parse_duration(duration_str) if duration_str else None
  until_date = datetime.utcnow() + timedelta(seconds=duration_seconds) if duration_seconds else None
  rights = ChatBannedRights(until_date=until_date, send_messages=False)
  current_rights = (await event.client.get_permissions(event.chat_id, entity)).send_messages
  if current_rights is True:
    return await event.edit(LANG['ALREADY_UNMUTED'])
  await event.client(EditBannedRequest(event.chat_id, entity, rights))
  await event.edit(LANG['UNMUTED'].format(entity.id))

@Neo.command(
  pattern='^ban ?(.*)',
  info=LANG['BAN_INFO'],
  usage='.ban <user>',
  example='.ban @username'
)
async def ban(event):
  user = await event.get_input_sender() if event.is_reply else event.pattern_match.group(1)
  duration_str = event.pattern_match.group(2)
  if not user:
    return await event.edit(LANG['NO_USER'])
  entity = await event.client.get_entity(user)
  duration_seconds = parse_duration(duration_str) if duration_str else None
  until_date = datetime.utcnow() + timedelta(seconds=duration_seconds) if duration_seconds else None
  rights = ChatBannedRights(until_date=until_date, view_messages=True)
  if not (await event.client.get_permissions(event.chat_id, entity)).view_messages:
    return await event.edit(LANG['ALREADY_BANNED'])
  await event.client(EditBannedRequest(event.chat_id, entity, rights))
  await event.edit(LANG['BANNED'].format(entity.id))

@Neo.command(
  pattern='^kick ?(.*)',
  info=LANG['KICK_INFO'],
  usage='.kick <user>',
  example='.kick @username'
)
async def kick(event):
  user = await event.get_input_sender() if event.is_reply else event.pattern_match.group(1)
  if not user:
    return await event.edit(LANG['NO_USER'])
  entity = await event.client.get_entity(user)
  try:
    await event.client(EditBannedRequest(event.chat_id, entity, ChatBannedRights(until_date=None, view_messages=True)))
    await event.client(EditBannedRequest(event.chat_id, entity, ChatBannedRights(until_date=None, view_messages=False)))
    return await event.edit(LANG['KICKED'].format(entity.id))
  except:
    return await event.edit(LANG['NOT_IN_GROUP'])

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
  entity = await event.client.get_entity(user)
  if (await event.client.get_permissions(event.chat_id, entity)).is_member:
    return await event.edit(LANG['ALREADY_IN_GROUP'])
  await event.client(InviteToChannelRequest(event.chat_id, [entity]))
  await event.edit(LANG['ADDED'].format(entity.id))

@Neo.command(
  pattern=r'^promote ?(.*)',
  info=LANG['PROMOTE_INFO'],
  usage='.promote <user>',
  example='.promote @username'
)
async def promote(event):
  user = await event.get_input_sender() if event.is_reply else event.pattern_match.group(1)
  if not user:
    return await event.edit(LANG['NO_USER'])
  entity = await event.client.get_entity(user)
  if (await event.client.get_permissions(event.chat_id, entity)).is_admin:
    return await event.edit(LANG['ALREADY_PROMOTED'])
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
  await event.client(EditAdminRequest(event.chat_id, entity, rights, "Admin"))
  await event.edit(LANG['PROMOTED'].format(entity.id))

@Neo.command(
  pattern=r'^demote ?(.*)',
  info=LANG['DEMOTE_INFO'],
  usage='.demote <user>',
  example='.demote @username'
)
async def demote(event):
  user = await event.get_input_sender() if event.is_reply else event.pattern_match.group(1)
  if not user:
    return await event.edit(LANG['NO_USER'])
  entity = await event.client.get_entity(user)
  if not (await event.client.get_permissions(event.chat_id, entity)).is_admin:
    return await event.edit(LANG['ALREADY_DEMOTED'])
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
  await event.client(EditAdminRequest(event.chat_id, entity, rights, "Admin"))
  await event.edit(LANG['DEMOTED'].format(entity.id))

@Neo.command(
  pattern='^pin(?:\s+(.*))?$',
  info=LANG['PIN_INFO'],
  usage='.pin [text]',
  example='.pin Hello World OR .pin (on reply)'
)
async def pin(event):
  text = event.pattern_match.group(1)
  if text == "undo" and event.reply_to_msg_id:
    try:
      await event.client.unpin_message(event.chat_id, event.reply_to_msg_id)
      return await event.edit(LANG['UNPINNED'])
    except Exception:
      return await event.edit(LANG['NOT_PINNED'])
  if text:
    sent = await event.client.send_message(event.chat_id, text)
    await event.client.pin_message(event.chat_id, sent.id)
    return await event.delete()
  if event.reply_to_msg_id:
    await event.client.pin_message(event.chat_id, event.reply_to_msg_id)
    return await event.edit(LANG['PINNED'])
  await event.edit(LANG['NO_MSG'])

@Neo.command(
  pattern='^revoke$',
  info=LANG['REVOKE_INFO'],
  usage='.revoke',
  example='.revoke'
)
async def revoke(event):
  new_link = await event.client(ExportChatInviteRequest(event.chat_id))
  await event.edit(LANG['REVOKED'].format(new_link.link))

@Neo.command(
  pattern='^link$',
  info=LANG['LINK_INFO'],
  usage='.link',
  example='.link'
)
async def link(event):
  link = await event.client(ExportChatInviteRequest(event.chat_id))
  await event.edit(LANG['LINK'].format(link.link))

@Neo.command(
  pattern='^open$',
  info=LANG['OPEN_INFO'],
  usage='.open',
  example='.open'
)
async def open_chat(event):
  rights = await event.client.get_chat_default_banned_rights(event.chat_id)
  if rights.send_messages is False:
    return await event.edit(LANG['ALREADY_OPEN'])
  new_rights = ChatBannedRights(send_messages=False)
  await event.client(EditChatDefaultBannedRightsRequest(event.chat_id, new_rights))
  await event.edit(LANG['OPENED'])

@Neo.command(
  pattern='^close$',
  info=LANG['CLOSE_INFO'],
  usage='.close',
  example='.close'
)
async def close_chat(event):
  rights = await event.client.get_chat_default_banned_rights(event.chat_id)
  if rights.send_messages is True:
    return await event.edit(LANG['ALREADY_CLOSED'])
  new_rights = ChatBannedRights(send_messages=True)
  await event.client(EditChatDefaultBannedRightsRequest(event.chat_id, new_rights))
  await event.edit(LANG['CLOSED'])
