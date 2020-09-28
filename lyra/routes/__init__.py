from .pages import pages

def register_blueprints(app):
  app.register_blueprint(pages)