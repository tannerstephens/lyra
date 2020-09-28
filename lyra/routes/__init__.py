from .auth import auth
from .lyra import lyra
from .pages import pages


def register_blueprints(app):
  app.register_blueprint(auth)
  app.register_blueprint(lyra)
  app.register_blueprint(pages)
