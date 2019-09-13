from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/<path:text>')
def react_view(text=None):
  return render_template('index.html.jinja2')
