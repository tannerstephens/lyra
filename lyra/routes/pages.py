from flask import Blueprint, flash, render_template, request, session, redirect, url_for
from ..decorators import login_required
from ..extensions import groupme_api
from ..models import Group

pages = Blueprint('pages', __name__)

@pages.route('/')
def home():
  return render_template('pages/home.html')

@pages.route('/groups')
@login_required
def groups_overview():
  gat = session['groupme_access_token']
  groups = Group.query.filter_by(owner=request.user).all()

  def get_group_data(group):
    group_id = group.groupme_id
    return groupme_api.group(group_id, gat)

  groups = map(get_group_data, groups)
  return render_template('pages/overview.html', groups=groups)

@pages.route('/groups/new')
@login_required
def list_groups():
  gat = session['groupme_access_token']
  groups = groupme_api.groups(gat)
  return render_template('pages/enroll.html', groups=groups)

@pages.route('/groups/<string:group_id>')
@login_required
def manage_group(group_id):
  gat = session['groupme_access_token']

  try:
    group = groupme_api.group(group_id, gat)
  except:
    return redirect(url_for('pages.groups_overview'))

  db_group = Group.query.filter_by(groupme_id=group['id']).first()

  if db_group is None:
    db_group = Group(groupme_id=group['id'], owner=request.user).save()

  if db_group.owner is not request.user:
    return redirect(url_for('pages.groups_overview'))

  return render_template('pages/manage.html', group=group)
