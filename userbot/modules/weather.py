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
    await event.reply(f"__City__ : **{data["name"]}**\n__Weather__ : **{data["weather"][0]["main"]}**\n__Climate__ : **{data["weather"][0]["description"]}**\n__Temperature__ : **{data["main"]["temp"]}°C**\n__Pressure__ : **{data["main"]["pressure"]} hPa**\n__Humidity Level__ : **{data["main"]["humidity"]}%**\n__Visibility__ : **{data["visibility"]} meters**\n__Wind Speed__ : **{data["wind"]["speed"]} m/s**\n__Wind Direction__ : **{data["wind"]["deg"]}°**\n__Cloudiness__ : **{data["clouds"]["all"]}%**")
