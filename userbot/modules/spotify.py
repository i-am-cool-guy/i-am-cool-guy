from userbot import Neo
from userbot.utils import lang, spotify_search

LANG = lang('spotify')

@Neo.command(
    pattern='^spotify ?(.*)',
    info=LANG["SPOTIFY_INFO"],
    usage='.spotify <track>',
    example='.spotify husn'
)
async def spotify(event):
  text = event.pattern_match.group(1) or False
  if text == False:
    return await event.edit(LANG["SPOTIFY_NONE"])
  data = spotify_search(text)
  info = False
  for track in data:
    if track["type"] == "track":
      duration_seconds = track['duration'] // 1000
      minutes = duration_seconds // 60
      seconds = duration_seconds % 60
      mmss_duration = f"{minutes}:{seconds:02}"
      info = LANG["SPOTIFY_TRACK"].format(track["title"], mmss_duration, '-'.join(reversed(track["release_date"].split('-'))), ', '.join([f"[{artist['name']}]({artist['url']})" for artist in track['artists']]), "Yes" if track["explicit"] == True else "No", track["popularity"], track["track_url"])
  if not info:
    return await event.edit(LANG["SPOTIFY_FAILED"])
  return await Neo.send_file(event.chat_id,
    file=track['images'][0]['url'],
    caption=info,
    parse_mode='md'
  )
