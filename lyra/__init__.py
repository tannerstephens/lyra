from flask import Flask
from flask_migrate import Migrate

def create_app(config='lyra.config.Config'):
  app = Flask(__name__)

  app.config.from_object(config)

  with app.app_context():
    from lyra.views import views
    app.register_blueprint(views)

    from lyra.api import api
    app.register_blueprint(api)

    from lyra.models import db
    migrate = Migrate(app, db)

  return app
