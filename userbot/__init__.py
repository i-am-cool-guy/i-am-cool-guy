from telethon import events
from telethon.sync import TelegramClient, custom
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
from datetime import datetime
import traceback, os, re

VERSION = 'v1.0'
CHANNEL = 'TheNeoTG'
SUPPORT = 'NeoSupportChat'

API_ID = os.getenv('API_ID', "20949887")
API_HASH = os.getenv('API_HASH', "70106464072168cc5893a74596935c43")
STRING_SESSION = os.getenv('STRING_SESSION', "1BVtsOIYBu4w0u2zkrmpyFFJUn1I5SPBbiSrPV0ZQpaisqnmdSvp5rMawUOO4Z3YTy2cC3ONkXlXlZFsdqdtx1K9FmCo4Tk-oE97_MfXkp3CnPp06lmOOIytxhdxEthvUHA1x2cG81pczYCUOv1Z1Fyw1DM38g0CcNtr_nmWsjukPwK2ZUGlYAYyp0PlUeOnrgNs9X13Uh4sVjFr-RIOs21UQXc547MS2DLj5spZwlEO4DW4RFN_T-yY6_iYTuQwu1QL9H6DUh1o76d5o8N8W7E2vq0juXX2QsJRnPEdM5doiz3tS93r9vxqjj9po5MQfeivo4VxVS1v_NFSLjTEJ1EOj1k4o7C0=")
PREFIX = os.getenv('PREFIX', ".")
LANGUAGE = os.getenv('LANGUAGE', 'en').lower()
AUTO_BIO = os.getenv('AUTO_BIO', False)
if isinstance(AUTO_BIO, str):
  AUTO_BIO = AUTO_BIO.lower()
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID', "04b268d298a04571bd32d727e909ad46") # For spotify search
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET', "65bbcb2166254570bb1489f9e34e2373") # For spotify search
SPOTIFY_ACCESS_TOKEN = os.getenv('SPOTIFY_ACCESS_TOKEN', "BQBpAvJMw2mjNRyR447HK4J2KgVKKW_FlETpaVziaJJewN3wzZSMgN5rrrm6SpGLhnfI0FBkg3BAfQH0ywdfBUbdLEyf48Iwkn-a8aysvGA6co7ratLj_HZa0y1cZBppmG60_21BVM3qfzZzp7vCDSse7csjBbrhmKY3rWau_kS4DiRzFai3iYhmO8P76FFYLhItMkiIUujC5QjpZwGu6VMUXAFRC5YoTPfQ5LzYvFlwuVJHCMF8kmJqN7fo67ajmxJSjcn4c0CU7gmE9WlKGqoy") # For last played
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
            'usage': usage.replace('.', PREFIX[0]) if usage != None else None,
            'example': example.replace('.', PREFIX[0]) if example != None else None,
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
