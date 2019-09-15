from .groupme_api import groupme_api
from .auth_api import auth_api

def register_api(app):
  app.register_blueprint(groupme_api, url_prefix='/v1/groupme')
  app.register_blueprint(auth_api, url_prefix='/v1/auth')
