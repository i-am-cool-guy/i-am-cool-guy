from telethon import events
from userbot import Neo, PREFIX
from userbot.utils import update, rollback, lang

LANG = lang('git')

@Neo.command(
  pattern='^update ?(.*)',
  info=LANG['UPDATE_INFO']
)
async def _update(event):
  text = event.pattern_match.group(1) or None
  if text == None or text != 'now':
    changelog = await update(True)
    if changelog:
      return await event.edit(LANG['CHANGELOG'].format(changelog, PREFIX))
  try: 
    status = await update(False)
  except ValueError:
    return await event.edit(LANG['UPDATE_FAILED'])
  await event.edit(LANG['UPDATING'])
  if status == False:
    return await event.edit(LANG['UP-TO-DATE'])
  return await event.reply(LANG['UPDATED'])

@Neo.command(
  pattern='^rollback ?(.*)',
  info=LANG['ROLLBACK_INFO']
)
async def _rollback(event):
  text = version = event.pattern_match.group(1) or None
  if text == None:
    return await event.edit(LANG['ROLLBACK_NONE'])
  if version == VERSION:
    return await event.edit(LANG['CURRENT_VER'].format(version))
  try: 
    status = await rollback(version)
  except ValueError:
    return await event.edit(LANG['ROLLBACK_FAILED'])
  await event.edit(LANG['ROLLING_BACK'].format(version))
  if status == False:
    return await event.edit(LANG['NO_VERSION'])
  return await event.reply(LANG['ROLLED_BACK'].format(version))
