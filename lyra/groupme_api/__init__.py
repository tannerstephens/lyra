import re
import requests

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
