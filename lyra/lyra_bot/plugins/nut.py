from random import randint

NAME = 'Nut'

HELP = '!nut'

NUT = '🥜'

def handle(data, groupme_api):
  if '!nut' in data['text'].lower():
    nuts = randint(1,10)
    groupme_api.send_message(data['group_id'], NUT*nuts)
