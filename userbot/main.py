from telethon.errors import PhoneNumberInvalidError
from telethon.tl.functions.account import UpdateProfileRequest
from userbot import Neo, AUTO_BIO
from userbot.utils import translate
from datetime import datetime
from time import sleep
import importlib.util
import os
import re

def load_dir(directory):
  for filename in os.listdir(directory):
    if filename.endswith('.py'):
      module_name = filename[:-3]
      file_path = os.path.join(directory, filename)
      spec = importlib.util.spec_from_file_location(module_name, file_path)
      module = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(module)

async def auto_bio(event):
  if AUTO_BIO == 'datetime':
    while True:
      time = datetime.now().strftime('%I:%M:%S %p')
      date = datetime.now().strftime('%A, %B %d, %Y')
      bio = f'📅 {date} ⏰ {time}'
      await Neo(UpdateProfileRequest(about=bio))
      sleep(1)

try:
  Neo.start()
  Neo.send_message('me', '**Neo is active!**')
except PhoneNumberInvalidError:
  print('Invalid phone number!');
  quit(0)

load_dir('userbot/modules')
Neo.add_event_handler(auto_bio)
Neo.run_until_disconnected()
