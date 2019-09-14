from flask import Blueprint, render_template, session, url_for, redirect, current_app, request

views = Blueprint('views', __name__)

@views.route('/login')
def login():
  client_id = current_app.config.get('GROUPME_CLIENT_ID')
  url = 'https://oauth.groupme.com/oauth/authorize?client_id={}'.format(client_id)

  return redirect(url)


@views.route('/login/callback')
def login_callback():
  access_token = request.args.get('access_token')

  session['access_token'] = access_token
  
  return redirect(url_for('views.react_view'))

@views.route('/logout')
def logout():
  session.clear()

  return redirect(url_for('views.react_view'))

@views.route('/')
@views.route('/<path:text>')
def react_view(text=None):
  return render_template('index.html.jinja2')
