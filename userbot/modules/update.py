from telethon import events
from userbot import Neo
from userbot.utils import update, lang
LANG = {
  'UPDATE_INFO': 'Updates Neo to latest version.',
  'UPDATING': '`Updating...`',
  'UP-TO-DATE': '**Neo is up-to-date.**',
  'UPDATE_FAILED': '**Failed to update Neo!**',
  'UPDATED': '**Neo is updated.**'
}

@Neo.command(
  pattern='^update ?(.*)',
  info=LANG['UPDATE_INFO']
)
async def update(event):
  text = event.pattern_match.group(1) or None
  if text == None or text != 'now':
    return await event.edit(
      await update(True)
    )
  status = await update()
  await event.edit(LANG['UPDATING'])
  if status == 'up-to-date':
    return await event.edit(LANG['UP-TO-DATE'])
  else if status == 'failed':
    return await event.edit(LANG['UPDATE_FAILED'])
  return await event.reply(LANG['UPDATED'])
