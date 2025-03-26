from git import Repo, GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import Spotify
from aiohttp import ClientSession
from googletrans import Translator
from rsnchat import RsnChat
from userbot import VERSION, LANGUAGE, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from os import path
import asyncio, sys, json

modules = path.join(path.dirname(__file__), '..', 'requirements.txt')
versions = path.join(path.dirname(__file__), '..', 'versions.json')

if not SPOTIFY_CLIENT_ID == False and not SPOTIFY_CLIENT_SECRET == False:
  spotify = Spotify(
    client_credentials_manager=SpotifyClientCredentials(
      SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
    )
  )
else:
  spotify = False

def spotify_search(track):
  def extract_artist_info(artist):
    return {
      'name': artist.get('name', 'N/A'),
      'url': artist.get('external_urls', {}).get('spotify', 'N/A')
    }
  def extract_image_info(image):
    return {
      'url': image.get('url', 'N/A'),
      'height': image.get('height', 'N/A'),
      'width': image.get('width', 'N/A')
    }
  if spotify == False:
    return spotify
  result = spotify.search(track)
  results_info = []

  for item in result.get('tracks', {}).get('items', []):
    album_info = item.get('album', {})
    track_info = {
      'title': item.get('name', 'N/A'),
      'id': item.get('id', 'N/A'),
      'type': item.get('type', 'N/A'),
      'release_date': album_info.get('release_date', 'N/A'),
      'artists': [extract_artist_info(artist) for artist in item.get('artists', [])],
      'images': [extract_image_info(image) for image in album_info.get('images', [])],
      'duration': item.get('duration_ms', 0),
      'explicit': item.get('explicit', False),
      'popularity': item.get('popularity', 0),
      'preview_url': item.get('preview_url', 'N/A'),
      'track_url': item.get('external_urls', {}).get('spotify', 'N/A')
    }

  results_info.append(track_info)

  for item in result.get('albums', {}).get('items', []):
    album_info = {
      'title': item.get('name', 'N/A'),
      'id': item.get('id', 'N/A'),
      'type': item.get('type', 'N/A'),
      'release_date': item.get('release_date', 'N/A'),
      'artists': [extract_artist_info(artist) for artist in item.get('artists', [])],
      'images': [extract_image_info(image) for image in item.get('images', [])],
      'total_tracks': item.get('total_tracks', 0),
      'album_url': item.get('external_urls', {}).get('spotify', 'N/A')
    }

    results_info.append(album_info)

  return results_info

async def update(changelog):
  try:
    repo = Repo()
  except (NoSuchPathError, GitCommandError, InvalidGitRepositoryError) as error:
    ValueError(error)

  active_branch = repo.active_branch
  if active_branch.name != 'main':
    ValueError('Updation Failed.')
  try:
    upstream_remote = repo.remote('upstream')
  except ValueError:
    upstream_remote = repo.create_remote('upstream', 'https://github.com/i-am-cool-guy/i-am-cool-guy.git')
  upstream_remote.fetch('main')

  changelog_str = ''
  for commit in repo.iter_commits(f'HEAD..upstream/main'):
    print(commit)
    changelog_str += f"• [{commit.committed_datetime.strftime('%d-%m-%y')}]: {commit.summary} <{commit.author}>\n"
  if changelog == True:
    return changelog_str
  if not changelog_str:
    return False
  else:
    try:
      upstream_remote.pull('main')
    except GitCommandError:
      repo.git.reset("--hard", "FETCH_HEAD")
      ValueError(GitCommandError)

    await update_requirements()
    return True

async def rollback(version):
  try:
    repo = Repo()
  except (NoSuchPathError, GitCommandError, InvalidGitRepositoryError) as error:
    ValueError(error)

  with open('versions.json', 'r') as f:
    versions = json.load(f)
    if version not in versions:
      return False
    commit_hash = versions[version]

    try:
      repo.git.reset("--hard", commit_hash)
    except GitCommandError as e:
      ValueError(e)

    return await update_requirements()

async def update_requirements():
  try:
    process = await asyncio.create_subprocess_exec(
     sys.executable, "-m", "pip", "install", "-r", requirements_path,
       stdout=asyncio.subprocess.PIPE,
       stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
      raise Exception(stderr.decode())
    else:
      return True
  except Exception as e:
    print(e)

async def request(method, url):
  async with ClientSession() as session:
    async with getattr(session, method)(url, headers={
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }) as response:
      return response

def translate(text, lang_to=LANGUAGE):
  translator = Translator()
  translation = translator.translate(text, dest=lang_to)
  return translation if isinstance(text, list) else translation.text

def ai(ai, text):
  conn = RsnChat('rsnai_1WZBGHRi6kA4cjyKNrZTuEVY') # Replace the key with yours, refer https://pypi.org/project/rsnchat/
  try:
    res = getattr(conn, ai)(text)
    return res.get('message', False)
  except Exception as e:
    return False

def lang(key):
  try:
    with open(f'userbot/language/{LANGUAGE}.json', 'r') as file:
      data = json.load(file)
      return data.get(key, {})
  except KeyError:
    print("All the strings aren't mentioned in selected language. Please use another language or add (in the json file of your language):")
    print(key)
