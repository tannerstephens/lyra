from flask import Flask
from .extensions import (
  db,
  migrate
)


def create_app(config='lyra.config.Config'):
  app = Flask(__name__)
  app.config.from_object(config)

  register_extensions(app)

  return app


def register_extensions(app):
  db.init_app(app)
  migrate.init_app(app)
