from telethon import events 
from userbot import Neo
from userbot.utils import lang, request
from aiocache import Cache
import asyncio
import os

LANG = lang('weather')

@Neo.command(
    pattern='^weather ?(.*)',
    info=LANG['WEATHER_INFO']
)
async def weather(event):
    text = event.pattern_match.group(1) or False
    if not text:
        return await event.reply(LANG['WEATHER_NONE'])
    cache = Cache(Cache.MEMORY)
    with asyncio.Runner() as runner:
      data = runner.run(cache.get(text))
      if data:
        data = json.loads(data)
        return await event.reply(
          LANG['WEATHER'].format(data["name"], data["weather"][0]["main"], data["weather"][0]["description"], data["main"]["temp"], data["main"]["pressure"], data["main"]["humidity"], data["visibility"], data["wind"]["speed"], data["wind"]["deg"], data["clouds"]["all"])
        )
      else:
        data = await request('get', f"http://api.openweathermap.org/data/2.5/weather?q={text}&units=metric&appid=060a6bcfa19809c2cd4d97a212b19273&language=en", 'json')
        runner.run(cache.set(text, json.dumps(data)))
        return await event.reply(
          LANG['WEATHER'].format(data["name"], data["weather"][0]["main"], data["weather"][0]["description"], data["main"]["temp"], data["main"]["pressure"], data["main"]["humidity"], data["visibility"], data["wind"]["speed"], data["wind"]["deg"], data["clouds"]["all"])
        )
