import requests

BASE_URL = 'https://api.groupme.com/v3/{endpoint}?token={token}'


class GroupmeApi:
  def __init__(self, access_token):
    self.access_token = access_token

  def _make_url(self, endpoint):
    stripped_endpoint = endpoint.strip('/')

    return BASE_URL.format(
      endpoint=stripped_endpoint,
      token=self.access_token
    )

  def _parse_response(self, response):
    return response.json().get('response')

  def get_groups(self, page=1):
    url = self._make_url('/groups')

    resp = requests.get(url, params={
      'page': page,
      'omit': 'memberships'
    })

    return self._parse_response(resp)

  def get_group(self, group_id):
    url = self._make_url('/groups/{}'.format(group_id))

    resp = requests.get(url)

    return self._parse_response(resp)

  def get_members(self, group_id):
    group = self.get_group(group_id)

    return group.get('members')

  def get_current_user(self):
    url = self._make_url('/users/me')

    resp = requests.get(url)

    return self._parse_response(resp)
