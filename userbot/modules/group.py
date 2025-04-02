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
    if not time_str:
        return None
    match = re.match(r"(\d+)([smhd])", time_str)
    if match:
        value, unit = int(match[1]), match[2]
        return {
            "s": timedelta(seconds=value),
            "m": timedelta(minutes=value),
            "h": timedelta(hours=value),
            "d": timedelta(days=value),
        }.get(unit)
    return None

async def is_admin(event):
    user = await event.client.get_me()
    admins = await event.client.get_participants(event.chat_id, filter=ChannelParticipantsAdmins)
    if user.id not in [admin.id for admin in admins]:
        await event.edit(LANG['NOT_ADMIN'])
        return False
    return True

async def get_user(event):
    if event.is_reply:
        return (await event.get_reply_message()).sender_id
    user = event.pattern_match.group(1)
    return await Neo.get_entity(user) if user else None

@Neo.command(
    pattern=r'^mute (\S+)\s*(\d+[smhd]?)?',
    info=LANG['MUTE_INFO'],
    usage='.mute <user> <duration (optional)>',
    example='.mute @username 10m'
)
async def mute(event):
    if not await is_admin(event):
        return
    
    user_input = event.pattern_match.group(1)
    duration_input = event.pattern_match.group(2)
    
    user = await Neo.get_entity(user_input)
    if not user:
        return await event.edit(LANG['NO_USER'])
    
    duration = parse_time(duration_input)
    rights = ChatBannedRights(until_date=duration, send_messages=True)
    
    await event.client(EditBannedRequest(event.chat_id, user.id, rights))
    mute_type = f"for {duration_input}" if duration_input else "permanently"
    await event.edit(f"Muted {user.username or user.id} {mute_type}.")

@Neo.command(
    pattern='^unmute (\S+)',
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
    await event.client(EditBannedRequest(event.chat_id, user, rights))
    await event.edit(LANG['UNMUTED'].format(user))

@Neo.command(
    pattern='^ban (\S+)',
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
    await event.client(EditBannedRequest(event.chat_id, user, rights))
    await event.edit(LANG['BANNED'].format(user))

@Neo.command(
    pattern='^kick (\S+)',
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
    await event.client(EditBannedRequest(event.chat_id, user, rights))
    await event.client(EditBannedRequest(event.chat_id, user, ChatBannedRights(view_messages=False)))
    await event.edit(LANG['KICKED'].format(user))

@Neo.command(
    pattern='^add (\S+)',
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
    
    await event.client(InviteToChannelRequest(event.chat_id, [user]))
    await event.edit(LANG['ADDED'].format(user))

@Neo.command(
    pattern=r'^promote (\S+)\s*(\S+)?',
    info=LANG['PROMOTE_INFO'],
    usage='.promote <user> <permissions (optional)>',
    example='.promote @username pin_messages'
)
async def promote(event):
    if not await is_admin(event):
        return
    
    user_input = event.pattern_match.group(1)
    permissions_input = event.pattern_match.group(2)
    
    user = await Neo.get_entity(user_input)
    if not user:
        return await event.edit(LANG['NO_USER'])
    
    rights = ChatAdminRights(**{permissions_input: True}) if permissions_input else ChatAdminRights(post_messages=True, add_admins=False, pin_messages=True)
    await event.client(EditAdminRequest(event.chat_id, user.id, rights, LANG['PROMOTED']))
    await event.edit(LANG['PROMOTED'].format(user))
