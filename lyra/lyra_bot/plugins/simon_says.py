NAME = 'Simon Says'

def handle(data, groupme_api):
  if '!say' == data['text'].lower()[:4]:
    message = data['text'][4:]

    mentions = list(filter(lambda attachment: attachment['type'] == 'mentions', data['attachments']))

    pre_strip_length = len(message)

    message = message.strip()

    if mentions:
      mentions = mentions[0]
      delta = 4 + (pre_strip_length - len(message))

      locations = mentions['loci']

      new_locations = []

      for location in locations:
        new_locations.append([
          location[0] - delta,
          location[1] - delta
        ])

      attachments = [
        {
          'loci': new_locations,
          'user_ids': mentions['user_ids'],
          'type': 'mentions'
        }
      ]
    else:
      attachments = None

    groupme_api.send_message(data['group_id'], message, attachments)
