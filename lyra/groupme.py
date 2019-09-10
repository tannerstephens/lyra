import requests

BASE_URL = 'https://api.groupme.com/v3/{endpoint}?{token}'

class GroupmeApi:
  def __init__(self, access_token):
    self.access_token = access_token

  def _make_url(self, endpoint):
    stripped_endpoint = endpoint.strip('/')

    return BASE_URL.format(
      endpoint=stripped_endpoint,
      token=self.access_token
    )

  def list_groups(self):
    url = self._make_url('/groups')
    resp = requests.get()
