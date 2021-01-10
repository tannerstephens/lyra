from requests import get
from threading import Thread
from time import sleep

NAME = 'Tell Jokes'

JOKE_URL = 'https://v2.jokeapi.dev/joke/Miscellaneous,Dark,Pun?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=twopart'

def handle(data, groupme_api):
  if '!joke' in data['text'].lower():
    joke = get(JOKE_URL).json()

    groupme_api.send_message(data['group_id'], joke['setup'])


def start_delivery_thread(data, joke, groupme_api):
  thread = Thread(target=delivery, args=(data, joke, groupme_api))
  thread.start()

def delivery(data, joke, groupme_api):
  sleep(5)
  groupme_api.send_message(data['group_id'], joke['delivery'])
