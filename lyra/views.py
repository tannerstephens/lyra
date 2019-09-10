from flask import Blueprint, render_template, request, redirect, current_app, url_for, session
from lyra.groupme import GroupmeApi
from lyra.models import User, db

views = Blueprint('views', __name__)

@views.route('/')
def home():
  if session.get('user_id'):
    return render_template('pages/home.html.jinja')
  else:
    return render_template('pages/not_logged_in.html.jinja')

@views.route('/login')
def login():
  client_id = current_app.config.get('GROUPME_CLIENT_ID')
  url = 'https://oauth.groupme.com/oauth/authorize?client_id={}'.format(client_id)
  return redirect(url)

@views.route('/login/callback')
def login_callback():
  access_token = request.args.get('access_token')
  
  if access_token:
    gapi = GroupmeApi(access_token)

    user_details = gapi.get_current_user()

    groupme_id = user_details.get('id')
    user = User.query.filter_by(groupme_id=groupme_id).first()

    if not user:
      user = User()

    user.groupme_id = groupme_id
    user.image_url = user_details.get('image_url')

    db.session.add(user)
    db.session.commit()

    session['user_id'] = user.id
    session['access_token'] = access_token

  return redirect(url_for('views.home'))
