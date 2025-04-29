from userbot import Neo
from userbot.utils import lang, spotify_search

LANG = lang('spotify')

@Neo.command(
    pattern='^spotify ?(.*)',
    info="Search spotify track.",
    usage='.spotify <track>',
    example='.spotify husn'
)
async def spotify(event):
  text = event.pattern_match.group(1) or False
  if text == False:
    return await event.edit("__Provide a track.__")
  await event.edit("```Downloading ...```")
  data = spotify_search(text)
  print(data)
