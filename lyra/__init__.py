from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

def create_app(config='lyra.config.Config'):
  app = Flask(__name__)
  CORS(app)

  app.config.from_object(config)

  with app.app_context():
    from lyra.api import register_api
    register_api(app)

    from lyra.models import db
    migrate = Migrate(app, db)

  return app
