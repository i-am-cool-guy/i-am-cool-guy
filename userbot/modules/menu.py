from telethon import events
from userbot import Neo, COMMANDS, PREFIX
from userbot.utils import lang
LANG = lang('menu')

@Neo.command(
  pattern='^menu ?(.*)',
  info='The list of commands.',
  hide=True
)
async def menu(event):
  menu = ''
  for command in COMMANDS:
    hide = command.get('hide', False)
    if not hide:
      cmd = command.get('command', False)
      info = command.get('info', False)
      usage = command.get('usage', False)
      example = command.get('example', False)
      if cmd and info:
        menu += f'**{LANG["COMMAND"]}:** `{PREFIX[0]}{cmd}`\n'
        menu += f'**{LANG["INFO"]}:** `{info}`\n'
        if usage:
          menu += f'**{LANG["USAGE"]}:** `{usage}`\n'
        if example:
          menu += f'**{LANG["EXAMPLE"]}:** `{example}`\n'
        menu += '\n'
  if menu:
    await event.edit(menu.strip())
  else:
    await event.edit(f'**{LANG["MENU_FAILED"]}**')
