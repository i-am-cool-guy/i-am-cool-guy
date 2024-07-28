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
async def _update(event):
  text = event.pattern_match.group(1) or None
  if text == None or text != 'now':
    return await event.edit(
      await update(True)
    )
  try: 
    status = await update(False)
  except ValueError:
    return await event.edit(LANG['UPDATE_FAILED'])
  await event.edit(LANG['UPDATING'])
  if status == False:
    return await event.edit(LANG['UP-TO-DATE'])
  return await event.reply(LANG['UPDATED'])
