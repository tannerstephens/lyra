import base64
import random
from threading import Thread

import requests

NAME = 'Craiyon'
HELP = 'Generate AI images with !craiyon'

CRAIYON_URL = 'https://backend.craiyon.com/generate'

def handle(data, groupme_api):
  if '!craiyon' == data['text'].lower()[:8]:
    request = data['text'][8:].strip()

    groupme_api.send_message(data['group_id'], 'Sure thing! This will take a bit.')
    start_generator_thread(data, request, groupme_api)

def start_generator_thread(data, request, groupme_api):
  thread = Thread(target=generate_image, args=(data, groupme_api, request,))
  thread.start()

def generate_image(data, groupme_api, request):
    resp = requests.post(CRAIYON_URL, json={'prompt': f'{request}<br>'})
    images = resp.json()['images']

    image = random.choice(images)
    binary_data = base64.b64decode(image)

    image_url = groupme_api.upload_image(binary_data, mime_type='image/webp')

    attachments = [
      {
        'type': 'image',
        'url': image_url
      }
    ]

    groupme_api.send_message(data['group_id'], '', attachments)
