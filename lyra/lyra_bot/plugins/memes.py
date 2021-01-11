from requests import get

NAME = 'Random Memes'

HELP = 'Get a fresh meme with !meme'

MEME_API = 'https://meme-api.herokuapp.com/gimme'

def handle(data, groupme_api):
  if '!meme' in data['text'].lower():
    meme = get(MEME_API).json()

    meme_url = meme['url']

    groupme_api.send_message(data['group_id'], meme_url)
