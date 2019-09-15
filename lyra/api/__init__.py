from .groupme_api import groupme_api

def register_api(app):
  app.register_blueprint(groupme_api, url_prefix='/v1')
