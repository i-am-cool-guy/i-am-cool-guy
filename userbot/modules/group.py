from userbot import Neo
from userbot.utils import lang
from telethon.tl.functions.channels import EditBannedRequest, EditAdminRequest, InviteToChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.types import ChatBannedRights, ChatAdminRights

LANG = lang('group')

@Neo.command(
    pattern='^mute ?(.*)',
    info=LANG['MUTE_INFO'],
    usage='.mute <user>',
    example='.mute @username'
)
async def mute(event):
    user = await event.get_chat() if event.is_reply else event.pattern_match.group(1)
    if not user:
        return await event.edit(LANG['NO_USER'])
    rights = ChatBannedRights(until_date=None, send_messages=True)
    await event.client(EditBannedRequest(event.chat_id, user, rights))
    await event.edit(LANG['MUTED'].format(user))

@Neo.command(pattern='^unmute ?(.*)', info=LANG['UNMUTE_INFO'], usage='.unmute <user>', example='.unmute @username')
async def unmute(event):
    user = await event.get_chat() if event.is_reply else event.pattern_match.group(1)
    if not user:
        return await event.edit(LANG['NO_USER'])
    rights = ChatBannedRights(until_date=None, send_messages=False)
    await event.client(EditBannedRequest(event.chat_id, user, rights))
    await event.edit(LANG['UNMUTED'].format(user))

@Neo.command(pattern='^ban ?(.*)', info=LANG['BAN_INFO'], usage='.ban <user>', example='.ban @username')
async def ban(event):
    user = await event.get_chat() if event.is_reply else event.pattern_match.group(1)
    if not user:
        return await event.edit(LANG['NO_USER'])
    rights = ChatBannedRights(until_date=None, view_messages=True)
    await event.client(EditBannedRequest(event.chat_id, user, rights))
    await event.edit(LANG['BANNED'].format(user))

@Neo.command(pattern='^kick ?(.*)', info=LANG['KICK_INFO'], usage='.kick <user>', example='.kick @username')
async def kick(event):
    user = await event.get_chat() if event.is_reply else event.pattern_match.group(1)
    if not user:
        return await event.edit(LANG['NO_USER'])
    rights = ChatBannedRights(until_date=None, view_messages=True)
    await event.client(EditBannedRequest(event.chat_id, user, rights))
    await event.client(EditBannedRequest(event.chat_id, user, ChatBannedRights(until_date=None, view_messages=False)))
    await event.edit(LANG['KICKED'].format(user))

@Neo.command(pattern='^add ?(.*)', info=LANG['ADD_INFO'], usage='.add <user>', example='.add @username')
async def add(event):
    user = event.pattern_match.group(1)
    if not user:
        return await event.edit(LANG['NO_USER'])
    await event.client(InviteToChannelRequest(event.chat_id, [user]))
    await event.edit(LANG['ADDED'].format(user))

@Neo.command(pattern='^promote ?(.*)', info=LANG['PROMOTE_INFO'], usage='.promote <user>', example='.promote @username')
async def promote(event):
    user = await event.get_chat() if event.is_reply else event.pattern_match.group(1)
    if not user:
        return await event.edit(LANG['NO_USER'])
    rights = ChatAdminRights(post_messages=True, add_admins=False, pin_messages=True)
    await event.client(EditAdminRequest(event.chat_id, user, rights, LANG['PROMOTED']))
    await event.edit(LANG['PROMOTED'].format(user))

@Neo.command(pattern='^demote ?(.*)', info=LANG['DEMOTE_INFO'], usage='.demote <user>', example='.demote @username')
async def demote(event):
    user = await event.get_chat() if event.is_reply else event.pattern_match.group(1)
    if not user:
        return await event.edit(LANG['NO_USER'])
    rights = ChatAdminRights(post_messages=False, add_admins=False, pin_messages=False)
    await event.client(EditAdminRequest(event.chat_id, user, rights, LANG['DEMOTED']))
    await event.edit(LANG['DEMOTED'].format(user))

@Neo.command(pattern='^pin$', info=LANG['PIN_INFO'], usage='.pin', example='.pin')
async def pin(event):
    if not event.reply_to_msg_id:
        return await event.edit(LANG['NO_MSG'])
    await event.client.pin_message(event.chat_id, event.reply_to_msg_id)
    await event.edit(LANG['PINNED'])

@Neo.command(pattern='^revoke$', info=LANG['REVOKE_INFO'], usage='.revoke', example='.revoke')
async def revoke(event):
    link = await event.client(ExportChatInviteRequest(event.chat_id))
    await event.edit(LANG['REVOKED'].format(link))

@Neo.command(pattern='^link$', info=LANG['LINK_INFO'], usage='.link', example='.link')
async def link(event):
    link = await event.client(ExportChatInviteRequest(event.chat_id))
    await event.edit(LANG['LINK'].format(link))

@Neo.command(pattern='^open$', info=LANG['OPEN_INFO'], usage='.open', example='.open')
async def open_chat(event):
    rights = ChatBannedRights(until_date=None, send_messages=False)
    await event.client(EditBannedRequest(event.chat_id, event.chat_id, rights))
    await event.edit(LANG['OPENED'])

@Neo.command(pattern='^close$', info=LANG['CLOSE_INFO'], usage='.close', example='.close')
async def close_chat(event):
    rights = ChatBannedRights(until_date=None, send_messages=True)
    await event.client(EditBannedRequest(event.chat_id, event.chat_id, rights))
    await event.edit(LANG['CLOSED'])
