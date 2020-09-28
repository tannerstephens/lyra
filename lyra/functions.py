from .extensions import groupme_api

def add_lyra_to_group(group_id, groupme_auth_token, callback):
  email = groupme_api.me_data['email']
  groupme_api.add_user(group_id, 'Lyra', email, groupme_auth_token)
  return groupme_api.create_bot(group_id, 'Lyra Listener', callback)

def remove_lyra_from_group(group_id, groupme_auth_token, bot_id, membership_id):
  groupme_api.remove_bot(bot_id)
  return groupme_api.remove_user(group_id, membership_id, groupme_auth_token)

def get_membership_id(group, user_id):
  for member in group['members']:
    if member['user_id'] == user_id:
      return member['id']
