from telethon import events 
from userbot import Neo
from userbot.utils import lang, request
import os

LANG = lang('weather')

@Neo.command(
    pattern='^weather ?(.*)',
    info='Get weather of a specific place.'
)
async def weather(event):
    text = event.pattern_match.group(1) or False
    if not text:
        return await event.reply('**Please enter any place name!**')
    data = await request('get', f"http://api.openweathermap.org/data/2.5/weather?q={text}&units=metric&appid=060a6bcfa19809c2cd4d97a212b19273&language=en", 'json')
    print(data)
    await event.reply(f"""_City_ : **${data.name}*"
__Weather__ : **${data.weather[0].main}**
__Climate__ : **${data.weather[0].description}**
__Temperature__ : **${data.main.temp}°C**
__Pressure__ : **${data.main.pressure} hPa**
__Humidity Level__ : **${data.main.humidity}%**
__Visibility__ : **${data.visibility} meters**
__Wind Speed__ : **${data.wind.speed} m/s**
__Wind Direction__ : **${data.wind.deg}°**
__Cloudiness__ : **${data.clouds.all}%**""")
