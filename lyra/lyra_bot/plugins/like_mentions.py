NAME = 'Like Mentions'

def handle(data, groupme_api):
  if 'attachments' not in data:
    return

  mentions = list(filter(lambda attachment: attachment['type'] == 'mentions', data['attachments']))[0]

  if len(mentions) == 0:
    return

  if groupme_api.me_data['user_id'] not in mentions['user_ids']:
    return

  groupme_api.like_message(data['group_id'], data['id'])
