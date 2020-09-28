from flask import Blueprint, session, redirect, url_for
from ..extensions import groupme_api
from ..models import User

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login')
def login():
  gat = session.get('groupme_access_token')

  groupme_user_id = groupme_api.me(gat).get('id')

  user = User.query.filter_by(groupme_id=groupme_user_id).first()

  if user is None:
    user = User(groupme_id=groupme_user_id).save()

  session['user_id'] = user.id

  return redirect(url_for('pages.groups_overview'))
