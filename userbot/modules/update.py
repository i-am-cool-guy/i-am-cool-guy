from telethon import events
from userbot import Neo
from userbot.utils import update, rollback, lang

LANG = {
  'UPDATE_INFO': 'Updates Neo to latest version.',
  'ROLLBACK_INFO': 'Rollbacks Neo to previous version.',
  'ROLLBACK_NONE': '**Please specify a version to rollback!**\n__For instance, 1.0, 1.1, 1.2 ...__',
  'UPDATING': '`Updating...`',
  'ROLLING_BACK': '`Rolling back to v{}`',
  'UP-TO-DATE': '**Neo is up-to-date.**',
  'NO_VERSION': '**No such version to rollback.**',
  'VERSION_DEP': '**Rolling back to v{} is no longer possible.**',
  'UPDATE_FAILED': '**Failed to update Neo!**',
  'ROLLBACK_FAILED': '**Failed to rollback Neo!**',
  'UPDATED': '**Neo is updated.**',
  'ROLLED_BACK': '**Neo rolled back to v{}.**'
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

@Neo.command(
  pattern='^rollback ?(.*)',
  info=LANG['ROLLBACK_INFO']
)
async def _rollback(event):
  text = version = event.pattern_match.group(1) or None
  if text == None:
    return await event.edit(LANG['ROLLBACK_NONE'])

  try: 
    status = await rollback(version)
  except ValueError:
    return await event.edit(LANG['ROLLBACK_FAILED'])
  await event.edit(LANG['ROLLING_BACK'])
  if status == False:
    return await event.edit(LANG['NO_VERSION'])
  return await event.reply(LANG['ROLLED_BACK'])
