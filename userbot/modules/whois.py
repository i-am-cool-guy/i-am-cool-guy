import os

from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
from userbot import Neo
from userbot.utils import lang

LANG = lang("whois")

@Neo.command(
  pattern="^whois ?(.*)",
  info="Get user details.",
  usage=".whois <reply/mention/id>",
  example=".whois @telegram"
)
async def whois(event):
  text = event.pattern_match.group(1)
  reply = await event.get_reply_message()
  user = (await Neo.get_me()).id
  if text and isinstance(text, int):
    user = int(event.pattern_match.group(1))
  elif reply:
    user = reply.from_id
  elif event.message.entities and isinstance(event.message.entities[0], MessageEntityMentionName):
    user = event.message.entities[0].user_id

  user = await Neo.get_entity(user)
  info = await Neo(GetFullUserRequest(user.id))
  result = (
        f"__ID:__ **{info.get('id')}**\n"
        f"__Is Bot:__ **{info.get('is_bot')}**\n"
        f"__Common Chats Count:__ **{info.get('common_chats_count')}**\n"
        f"__About:__ **{info.get('about')}**\n"
        f"__Profile Photo:__ **{info.get('profile_photo')}**\n"
        f"__Birthday:__ **{info.get('birthday')}**\n"
        f"__Personal Channel ID:__ **{info.get('personal_channel_id')}**\n"
        f"__Verified:__ **{info.get('verified')}**\n"
        f"__Restricted:__ **{info.get('restricted')}**\n"
        f"__Scam:__ **{info.get('scam')}**\n"
        f"__Premium:__ **{info.get('premium')}**\n"
        f"__First Name:__ **{info.get('first_name')}**\n"
        f"__Last Name:__ **{info.get('last_name')}**\n"
        f"__Phone Number:__ **{info.get('phone_number')}**\n"
        f"__Status:__ **{info.get('status')}**\n"
        f"__Photo:__ **{info.get('photo')}**\n"
    )
    
    if info.get("is_bot"):
        result += (
            f"__Bot Info Version:__ **{info.get('bot_info_version')}**\n"
            f"__Restriction Reason:__ **{info.get('restriction_reason')}**\n"
            f"__Bot Inline Placeholder:__ **{info.get('bot_inline_placeholder')}**\n"
            f"__Bot Attach Menu:__ **{info.get('bot_attach_menu')}**\n"
            f"__Bot Inline Geo:__ **{info.get('bot_inline_geo')}**\n"
            f"__Bot Can Edit:__ **{info.get('bot_can_edit')}**\n"
            f"__Bot Nochats:__ **{info.get('bot_nochats')}**\n"
            f"__Bot Business:__ **{info.get('bot_business')}**\n"
            f"__Bot Chat History:__ **{info.get('bot_chat_history')}**\n"
        )
  return await event.edit(result)
