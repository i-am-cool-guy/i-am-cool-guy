from time import time_ns
from telethon import events
from userbot import Neo, VERSION, CHANNEL, SUPPORT
from userbot.utils import lang, translate
import speedtest
import subprocess
LANG = lang('sys')

@Neo.command(
    pattern='^alive$',
    info=LANG['ALIVE_INFO']
)
async def alive(event):
  return await event.edit(
      LANG['ALIVE'].format(LANG[random.choice(["ALIVE_MSG1", "ALIVE_MSG2", "ALIVE_MSG3", "ALIVE_MSG4"])], VERSION, CHANNEL, SUPPORT, "https://github.com/TOXIC-DEVIL/Neo")
  )

@Neo.command(
    pattern='^ping$',
    info=LANG['PING_INFO']
)
async def ping(event):
  start = time_ns() // 1000000
  await event.edit('`Ping!`')
  stop = time_ns() // 1000000
  ms = stop - start
  return await event.edit('**Pong!**\n`' + str(ms) + 'ms`')

@Neo.command(
    pattern='^sys$',
    info=LANG['SYS_INFO']
)
async def system_stats(event):
  await event.edit(LANG['SYS_LOADING'])
  try:
    stats = (
      subprocess.run(['neofetch', '--stdout'], capture_output=True, text=True)
    ).stdout
  except Exception as e:
    await event.edit(LANG['SYS_FAILED'])
  await event.edit(stats)
    
@Neo.command(
    pattern='^speedtest$',
    info=LANG['SPEEDTEST_INFO']
)
async def speed_test(event):
  await event.edit(LANG['SPEEDTEST_LOADING'])
  speed = speedtest()
  speed.get_best_server()
  speed.download()
  speed.upload()
  results = speed.results.dict()
  download = results['download']
  upload = results['upload']
  average = (download + upload) / 2
  await event.edit(
    f'{LANG["DOWN_SPEED"]} **{download}**\n' + 
    f'{LANG["UPLOAD_SPEED"]} **{upload}**\n' +
    f'{LANG["AVG_SPEED"]} **{average}**'
  )
