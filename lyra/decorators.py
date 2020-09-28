from functools import wraps
from flask import flash, request, redirect, url_for

def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if request.user is None:
      return redirect(url_for('pages.home'))
    return f(*args, **kwargs)
  return decorated_function
