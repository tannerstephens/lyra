NAME = 'Force Rename'

HELP = 'Forcefully rename someone with !rename <name>'

DISABLED = True

def handle(data, groupme_api):
  if '!rename' == data['text'].lower()[:7]:
    new_name = data['text'][7:].strip()

    groupme_api.remove_user(data['group_id'], data['id'])
    groupme_api.add_user(data['group_id'], new_name, user_id=data['user_id'])
