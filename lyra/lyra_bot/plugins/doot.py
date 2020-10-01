NAME = 'Doot Doot'

def handle(data, groupme_api):
  if '!doot' in data['text'].lower():
    attachments = [
      {
        'type': 'image',
        'url': 'https://i.groupme.com/220x201.gif.c23c7eeaf31543ee8c10c5963d8c5a68'
      }
    ]

    groupme_api.send_message(data['group_id'], '', attachments)
