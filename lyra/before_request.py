from flask import session, g
from .models import User

def before_request(app):
  @app.before_request
  def add_user():
    if session.get('user_id'):
      user = User.query.filter_by(id=session.get('user_id')).first()

      if user is None:
        session.clear()
    else:
      user = None

    g.user = user
