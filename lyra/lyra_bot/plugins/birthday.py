from random import choice
from re import findall
from requests import get

NAME = 'Birthday'

HELP = 'Use !birthday <name> to have Lyra post a fun birthday video'

URL_BASE = 'https://epichappybirthdaysongs.com/{name}/'

HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
}

YOUTUBE_REGEX = r'href="(.+yout.+)"'

def handle(data, groupme_api):
  if '!birthday' == data['text'].lower()[:9]:
    name = data['text'][9:].split()[0].lower()

    url = URL_BASE.format(name=name)

    response = get(url, headers=HEADERS)

    youtube_urls = findall(YOUTUBE_REGEX, response.text)

    if len(youtube_urls) == 0:
      groupme_api.send_message(data['group_id'], 'Error: {} cannot have a birthday'.format(name))
      return

    chosen_url = choice(youtube_urls)

    message = 'Happy Birthday {name}!\n{url}'.format(name=name, url=chosen_url)

    groupme_api.send_message(data['group_id'], message)
