from flask import Flask
from os import path
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from .before_request import before_request
from .routes import register_blueprints
from .extensions import (
  db,
  migrate,
  groupme_oauth,
  groupme_api,
  lyra
)

def create_app(config='lyra.config.Config'):
  app = Flask(__name__)
  app.config.from_object(config)
  load_additional_config(app)

  register_extensions(app)
  register_blueprints(app)
  before_request(app)

  return app

def register_extensions(app):
  db.init_app(app)
  migrate.init_app(app, db)
  groupme_oauth.init_app(app, 'auth.login')
  groupme_api.init_app(app)
  lyra.init_app(app)

def load_additional_config(app):
  DIR = path.dirname(path.abspath(__file__))
  with open(f'{DIR}/config.yml') as f:
    config = load(f, Loader)

  app.config['GROUPME_CLIENT_ID'] = config['GROUPME_CLIENT_ID']
  app.config['GROUPME_ACCESS_TOKEN'] = config['GROUPME_ACCESS_TOKEN']
