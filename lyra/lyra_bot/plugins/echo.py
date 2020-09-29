from lyra.extensions import groupme_api

def handle(data):
  groupme_api.send_message(data['group_id'], data['text'])
