import requests

from json.decoder import JSONDecodeError
from uuid import uuid4

BASE_URL = 'https://api.groupme.com/v3{endpoint}'

class GroupmeAPI:
  def __init__(self, app=None):
    if app:
      self.init_app(app)

  def init_app(self, app):
    self._verify_config(app)
    self.access_token = app.config['GROUPME_ACCESS_TOKEN']

    self.me_data = self.me()

  def _verify_config(self, app):
    if 'GROUPME_ACCESS_TOKEN' not in app.config:
      raise Exception('Error! GROUPME_ACCESS_TOKEN must be in app config!')

  def _get_auth_header(self, access_token=None):
    access_token = access_token or self.access_token

    return {
      'X-Access-Token': access_token
    }

  def _get_endpoint(self, endpoint, access_token, params=None):
    header = self._get_auth_header(access_token)
    resp = requests.get(BASE_URL.format(endpoint=endpoint), headers=header, params=params)
    return self._verify_response(resp.json())

  def _post_endpoint(self, endpoint, json, access_token):
    header = self._get_auth_header(access_token)
    resp = requests.post(BASE_URL.format(endpoint=endpoint), headers=header, json=json)
    return self._verify_response(resp.json())

  def _verify_response(self, response):
    if 'response' not in response:
      raise Exception(f'Error! Invalid response from groupme! {response}')

    return response.get('response')

  def me(self, access_token=None):
    return self._get_endpoint('/users/me', access_token)

  def groups(self, access_token=None, omit_members=True, page=1):
    params = {'omit':'memberships'} if omit_members else {}
    params['page'] = page
    return self._get_endpoint('/groups', access_token, params)

  def group(self, group_id, access_token=None):
    return self._get_endpoint(f'/groups/{group_id}', access_token)

  def add_user(self, group_id, nickname, email, access_token=None):
    data = {
      'members': [
        {
          'nickname': nickname,
          'email': email
        }
      ]
    }

    results_id = self._post_endpoint(f'/groups/{group_id}/members/add', data, access_token)['results_id']
    return self._get_endpoint(f'/groups/{group_id}/members/results/{results_id}', access_token)

  def create_bot(self, group_id, name, callback, access_token=None):
    json = {
      'bot': {
        'name': name,
        'group_id': group_id,
        'callback_url': callback
      }
    }

    return self._post_endpoint('/bots', json, access_token)

  def remove_bot(self, bot_id, access_token=None):
    json = {
      'bot_id': bot_id
    }

    try:
      self._post_endpoint('/bots/destroy', json, access_token)
    except JSONDecodeError:
      return True

  def remove_user(self, group_id, membership_id, access_token=None):
    try:
      self._post_endpoint(f'/groups/{group_id}/members/{membership_id}/remove', None, access_token)
    except JSONDecodeError:
      return True

  def send_message(self, group_id, text=None, attachments=None, access_token=None):
    if attachments is None and text is None or text == '':
      raise Exception('Text cannot be blank if attachments is empty')
    json = {
      'message': {
        'source_guid': str(uuid4())
      }
    }

    if text:
      json['message']['text'] = text

    if attachments:
      json['message']['attachments'] = attachments

    return self._post_endpoint(f'/groups/{group_id}/messages', json, access_token)
