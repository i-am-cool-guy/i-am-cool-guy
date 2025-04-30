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
  info = f"""__Title:__ **{data[0].title}**\n
__Type:__ **{data[0].track}**
__Release date:__ **{(data[0].release_date).split("-").reverse()}**
__Artists:__ **{}**
__Explicit:__ **{"Yes" if data[0].explicit == True else "No"}**
__Popularity:__ **{data[0].popularity}**
__Track URL:__ {data.track_url}
"""
