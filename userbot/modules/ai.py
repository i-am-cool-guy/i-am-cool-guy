from userbot import Neo
from userbot.utils import ai, lang
LANG = lang('ai')

@Neo.command(
    pattern='^gpt ?(.*)',
    info=LANG['CHATGPT_INFO'],
    usage='.gpt <message>',
    example='.gpt Hello ChatGPT!'
)
async def chatgpt(event):
  text = event.pattern_match.group(1) or False
  if text == False:
    return await event.edit(LANG['AI_NONE'])
  await event.edit(LANG['THINK'])
  response = ai('gpt', text)
  return await event.edit('**' + response + '**')

@Neo.command(
    pattern='^gemini ?(.*)',
    info=LANG['GEMINI_INFO'],
    usage='.gemini <message>',
    example='.gemini Hello Gemini!'
)
async def gemini(event):
  text = event.pattern_match.group(1) or False
  if text == False:
    return await event.edit(LANG['AI_NONE'])
  await event.edit(LANG['THINK'])
  response = ai('gemini', text)
  return await event.edit('**' + response + '**')

@Neo.command(
    pattern='^mistral ?(.*)',
    info=LANG['MISTRAL_INFO'],
    usage='.mistral <message>',
    example='.mistral Hello Mistral!'
)
async def gemini(event):
  text = event.pattern_match.group(1) or False
  if text == False:
    return await event.edit(LANG['AI_NONE'])
  await event.edit(LANG['THINK'])
  response = ai('mixtral', text)
  return await event.edit('**' + response + '**')

@Neo.command(
    pattern='^llama ?(.*)',
    info=LANG['LLAMA_INFO'],
    usage='.llama <message>',
    example='.llama Hello LLaMa!'
)
async def gemini(event):
  text = event.pattern_match.group(1) or False
  if text == False:
    return await event.edit(LANG['AI_NONE'])
  await event.edit(LANG['THINK'])
  response = ai('llama', text)
  return await event.edit('**' + response + '**')
    
