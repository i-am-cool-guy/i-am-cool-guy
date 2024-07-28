from userbot import Neo
from userbot.utils import lang, request
LANG = lang('web')

@Neo.command(
    pattern='^define ?(.*)',
    info=LANG['DEF_INFO'],
    usage='.define <word>',
    example='.define contrary'
)
async def dict(event):
  text = event.pattern_match.group(1) or False
  if text == False:
    return await event.edit(LANG['DEF_NONE'])
  await event.edit(LANG['SEARCH'])
  data = await request('get', 'https://api.dictionaryapi.dev/api/v2/entries/en/' + text, 'json')
  if data:
    word = data[0]['word']
    phonetics = data[0]['phonetics'][0]['text'] if data[0]['phonetics'] else ''
    parts_of_speech = data[0]['meanings'][0]['partOfSpeech']
    definition = data[0]['meanings'][0]['definitions'][0]['definition']
    example = next((item.get('example', '') for item in data[0]['meanings'][0]['definitions'] if 'example' in item), '')
    rtext = (
      f"{LANG['WORD']} : **{word}**\n"
      f"{LANG['PHONETICS']} : **{phonetics}**\n"
      f"{LANG['POP']} : **{parts_of_speech}**\n"
      f"{LANG['DEF']} :\n**{definition}**"
    )
    if example:
      rtext += f"\n__{lang('menu')['EXAMPLE']}__ : **{example}**"
      await event.reply(rtext)
  else:
    await event.reply(LANG['DEF_FAILED'])
