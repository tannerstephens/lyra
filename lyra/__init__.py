from flask import Flask
from flask_migrate import upgrade
from .before_request import before_request
from .routes import register_blueprints
from .lyra_bot import lyra
from .extensions import (
  db,
  migrate,
  groupme_oauth,
  groupme_api
)

def create_app(config='lyra.config.Config'):
  app = Flask(__name__)
  app.config.from_object(config)

  with app.app_context():
    register_extensions(app)
    register_blueprints(app)
    before_request(app)
    lyra.init_app(app)

  return app

def register_extensions(app):
  db.init_app(app)
  migrate.init_app(app, db)
  upgrade()
  groupme_oauth.init_app(app, 'auth.login')
  groupme_api.init_app(app)

app = create_app()
