from flask import Flask

def create_app(config='lyra.config.Config'):
  app = Flask(__name__)

  app.config.from_object(config)

  with app.app_context():
    from lyra.views import views
    app.register_blueprint(views)

  return app
