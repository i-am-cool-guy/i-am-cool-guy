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
  text = event.pattern_match.group(0) or False
  if text == False:
    for command in COMMANDS:
      hide = command.get('hide', False)
      if not hide:
        cmd = command.get('command', False)
        info = command.get('info', False)
        if cmd and info:
          menu += f'**{PREFIX[0]}{cmd}**\n'
          menu += f'__{info}__\n\n'
  else:
    for command in COMMANDS:
      if text == command and command.get('hide', False) == False: 
        cmd = command.get('command', False)
        info = command.get('info', False)
        usage = command.get('usage', False)
        example = command.get('example', False)
        menu += f'**{cmd.upper()}**\n'
        menu += f'__{info}__\n\n'
        if usage:
          menu += f'```{usage}```'
        if example:
          menu += f'```{example}```'
        
  if menu != '':
    await event.edit(menu.strip())
  else:
    await event.edit(f'**{LANG["MENU_FAILED"]}**')
