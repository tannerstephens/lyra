from functools import wraps

from flask import Blueprint, render_template, request, redirect, current_app, url_for, session
from lyra.groupme import GroupmeApi
from lyra.models import User, db

views = Blueprint('views', __name__)

def logged_in(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    if not session.get('user_id', False):
      return redirect(url_for('views.home'))
    return func(*args, **kwargs)
  return wrapper

@views.context_processor
def inject_user():
  user_id = session.get('user_id')

  logged_in = False
  user = None

  if user_id:
    user = User.query.filter_by(id=user_id).first()

    if user:
      logged_in = True
    else:
      redirect(url_for('views.logout'))
  
  return dict(
    user = user,
    logged_in = logged_in
  )

@views.route('/')
def home():
  return render_template('pages/home.html.jinja')

@views.route('/manage')
@logged_in
def list_groups():
  groupme_token = session.get('access_token')
  gapi = GroupmeApi(groupme_token)

  page = int(request.args.get('page', 1))

  groups = gapi.get_groups(page)

  return render_template('pages/list_groups.html.jinja', groups=groups, page=page)

@views.route('/manage/<int:group_id>')
@logged_in
def manage_group(group_id):
  groupme_token = session.get('access_token')
  gapi = GroupmeApi(groupme_token)

  group = gapi.get_group(group_id)

  if not group:
    return redirect(url_for('views.list_groups'))

  return render_template('pages/manage_group.html.jinja', group=group)


@views.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('views.home'))

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
    user.name = user_details.get('name')

    db.session.add(user)
    db.session.commit()

    session['user_id'] = user.id
    session['access_token'] = access_token

  return redirect(url_for('views.home'))
