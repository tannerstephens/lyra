from .extensions import groupme_api

def add_lyra_to_group(group_id, groupme_auth_token, callback):
  email = groupme_api.me_data['email']
  groupme_api.add(group_id, 'Lyra', email, groupme_auth_token)
  groupme_api.create_bot(group_id, 'Lyra Listener', callback)
