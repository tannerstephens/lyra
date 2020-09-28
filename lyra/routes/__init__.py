from .auth import auth
from .pages import pages


def register_blueprints(app):
  app.register_blueprint(auth)
  app.register_blueprint(pages)
