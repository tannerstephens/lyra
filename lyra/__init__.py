from flask import Flask
from flask_migrate import Migrate

def create_app(config='lyra.config.Config'):
  app = Flask(__name__)

  app.config.from_object(config)

  with app.app_context():
    from lyra.api import register_api
    register_api(app)

    from lyra.views import views
    app.register_blueprint(views)

    from lyra.models import db
    migrate = Migrate(app, db)

  return app
