from userbot import Neo, LANGUAGE
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
  try:
    if data[0]:
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
        await event.edit(rtext)
  except KeyError:
      await event.edit(LANG['DEF_FAILED'])

@Neo.command(
    pattern="^wiki ?(.*)",
    info=LANG["WIKI_INFO"],
    usage=".wiki <article>",
    example=".wiki AI"
)
async def wikipedia(event):
  text = event.pattern_match.group(1)
  if not text:
    return await event.edit(LANG["WIKI_NONE"])
  data = await request('get', f"https://{LANGUAGE}.wikipedia.org/w/api.php?action=query&prop=extracts&titles={text}&exintro=&exsentences=10&explaintext=&redirects=&formatversion=2&format=json", 'json')
  #try:
  info = "**" + data["query"]["pages"][0]["title"] + "**\n\n__" + data["query"]["pages"][0]["extract"] + "__\n\n" + "https://en.wikipedia.org/wiki/" + data["query"]["pages"][0]["title"]
  return await event.edit(info)
  #except Error as e:
  #  raise ValueError(e)
  #  return await event.edit(LANG["WIKI_FAILED"])
