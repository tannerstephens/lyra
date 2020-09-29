import lyra
from lyra.extensions import groupme_api

NAME = 'Mention Everyone'

def handle(data):
  if '@everyone' in data['text'].lower():
    group = groupme_api.group(data['group_id'])
    members = list(map(lambda member: member['user_id'], group['members']))
    members.remove(groupme_api.me_data['user_id'])
    attachments = [
      {
        'loci': [[0, len(data['text'])]]*len(members),
        'user_ids': members,
        'type': 'mentions'
      }
    ]
    groupme_api.send_message(data['group_id'], data['text'], attachments)
