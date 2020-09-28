from functools import wraps
from flask import redirect, url_for, g

def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if g.user is None:
      return redirect(url_for('pages.home'))
    return f(*args, **kwargs)
  return decorated_function
