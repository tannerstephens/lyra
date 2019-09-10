from flask import Flask
from flask_migrate import Migrate

def create_app(config='lyra.config.Config'):
  app = Flask(__name__)

  app.config.from_object(config)

  with app.app_context():
    from lyra.views import views
    app.register_blueprint(views)

    from lyra.models import db
    if db.engine.url.drivername == 'sqlite':
      migrate = Migrate(app, db, render_as_batch=True)
    else:
      migrate = Migrate(app, db)

  return app
