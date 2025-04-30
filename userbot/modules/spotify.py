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
    return await event.edit("**Please enter a track!**")
  await event.edit("`Searching ...`")
  data = spotify_search(text)
  track = data[0]
  duration_seconds = track['duration'] // 1000
  minutes = duration_seconds // 60
  seconds = duration_seconds % 60
  mmss_duration = f"{minutes}:{seconds:02}"
  info = f"""__Title:__ **{track["title"]}**
__Type:__ **{track["type"]}**
__Duration:__ **{mmss_duration}**
__Release date:__ **{'-'.join(reversed(track["release_date"].split('-')))}**
__Artists:__ **{', '.join([f"[{artist['name']}]({artist['url']})" for artist in track['artists']])}**
__Explicit:__ **{"Yes" if track["explicit"] == True else "No"}**
__Popularity:__ **{track["popularity"]}**
__Track URL:__ {track["track_url"]}
"""
  return await Neo.send_file(event.chat_id,
    file=track['images'][0]['url'],
    caption=info,
    parse_mode='md'
  )
