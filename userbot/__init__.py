from telethon import events
from telethon.sync import TelegramClient, custom
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
from dotenv import load_dotenv
from datetime import datetime
import traceback, os, re

load_dotenv('config.env')

VERSION = 'v1.0'
CHANNEL = 'TheNeoTG'
SUPPORT = 'NeoSupportChat'

API_ID = os.getenv('API_ID', False)
API_HASH = os.getenv('API_HASH', False)
STRING_SESSION = os.getenv('STRING_SESSION', False)
PREFIX = os.getenv('PREFIX', False)
LANGUAGE = os.getenv('LANGUAGE', 'eng').lower()
AUTO_BIO = os.getenv('AUTO_BIO', False)
if isinstance(AUTO_BIO, str):
  AUTO_BIO = AUTO_BIO.lower()
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID', False) # For spotify search
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET', False) # For spotify search
SPOTIFY_ACCESS_TOKEN = os.getenv('SPOTIFY_ACCESS_TOKEN', False) # For last played
COMMANDS = []

if API_ID == False or API_HASH == False:
  print('Please provide the following environment variables:\n- API_ID\n-API_HASH');
  quit(0);
if PREFIX == False:
  print('You have not provided a prefix, default prefix are: .')
  PREFIX = '.'

if StringSession:
  Neo = TelegramClient(
    StringSession(STRING_SESSION), API_ID, API_HASH
  )
else:
  Neo = TelegramClient('Neo', API_ID, API_HASH)

def command(pattern=None, info=None, outgoing=True, usage=None, example=None, hide=False):
    def decorator(func):
        if not pattern or not info:
            raise ValueError('Both \'pattern\' and \'info\' must be provided.')
        cmd = pattern.strip('^\+\$\?\(\)\.\*')
        async def wrapper(event):
          try:
            await func(event)
          except Exception as e:
            error_message = (
              f"ERROR REPORT\n\n"
              f"Command: {cmd}\n"
              f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
              f"Traceback:\n"
              f"{traceback.format_exc()}"
            )
            print(traceback.format_exc())
            with open('userbot/temp/error_log.txt', 'w') as f:
              f.write(error_message)
            await Neo.send_file('me', 'userbot/temp/error_log.txt', caption=f"**An error occurred while using the `{cmd}` command. Please see the details in the attached error report. For further info, You can forward this error report to the [Neo Support Chat](tg://resolve?domain=NeoSupportChat).**")
            os.remove('userbot/temp/error_log.txt')

        Neo.on(events.NewMessage(outgoing=outgoing, pattern=pattern.replace("^", "^["+ PREFIX + "]")))(wrapper)
        Neo.on(events.MessageEdited(outgoing=outgoing, pattern=pattern.replace("^", "^[" + PREFIX + "]")))(wrapper)
        COMMANDS.append({
            'command': cmd,
            'info': info,
            'usage': usage,
            'example': example,
            'hide': hide,
        })
        return wrapper
    return decorator

try:
  Neo.start()
  Neo.command = command
  Neo(JoinChannelRequest("@NeoSupportChat"))
  Neo(JoinChannelRequest("@TheNeoTG"))
except Exception as e:
  pass
