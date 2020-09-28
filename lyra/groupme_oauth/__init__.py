from .register_blueprint import register_blueprint

class GroupmeOAuth:
  def __init__(self, app=None):
    if app:
      self.init_app(app)

  def init_app(self, app, callback_redirect):
    self._verify_config(app)
    self.client_id = app.config['GROUPME_CLIENT_ID']
    register_blueprint(app, callback_redirect)

  def _verify_config(self, app):
    if 'GROUPME_CLIENT_ID' not in app.config:
      raise Exception('Error! GROUPME_CLIENT_ID not defined in app config')
