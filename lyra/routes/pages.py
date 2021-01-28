from lyra.functions import add_lyra_to_group, remove_lyra_from_group, get_membership_id
from flask import Blueprint, flash, render_template, session, redirect, url_for, g, current_app, request
from ..decorators import login_required
from ..extensions import groupme_api
from ..models import Group, Plugin

pages = Blueprint('pages', __name__)

@pages.route('/')
def home():
  return render_template('pages/home.html')

@pages.route('/groups')
@login_required
def groups_overview():
  gat = session['groupme_access_token']
  groups = Group.query.filter_by(owner=g.user).all()

  def get_group_data(group):
    group_id = group.groupme_id
    return groupme_api.group(group_id, gat)

  groups = sorted(map(get_group_data, groups), key=lambda group: group['name'])
  return render_template('pages/overview.html', groups=groups)

@pages.route('/groups/new')
@login_required
def list_groups():
  gat = session['groupme_access_token']
  groups = groupme_api.groups(gat)
  return render_template('pages/enroll.html', groups=groups)

@pages.route('/groups/<string:group_id>')
@login_required
def group(group_id):
  gat = session['groupme_access_token']

  try:
    groupme_api.group(group_id, gat)
  except:
    return redirect(url_for('pages.groups_overview'))

  db_group = Group.query.filter_by(groupme_id=group_id).first()

  if db_group is None:
    callback = current_app.config['BASE_URL'] + '/lyra/'
    bot = add_lyra_to_group(group_id, gat, callback)
    db_group = Group(
      groupme_id=group_id,
      owner=g.user,
      bot_id=bot['bot']['bot_id']
    ).save()

  if db_group.owner is g.user:
    return redirect(url_for('pages.manage_group', group_id=group_id))
  else:
    return redirect(url_for('pages.view_group', group_id=group_id))

@pages.route('/groups/<string:group_id>/view')
@login_required
def view_group(group_id):
  gat = session['groupme_access_token']

  try:
    group = groupme_api.group(group_id, gat)
    print(group)
  except:
    return redirect(url_for('pages.groups_overview'))

  db_group = Group.query.filter_by(groupme_id=group_id).first()

  if db_group is None:
    return redirect(url_for('pages.group', group_id=group_id))

  if db_group.owner is g.user:
    return redirect(url_for('pages.manage_group'), group_id=group_id)

  plugins = Plugin.query.all()
  enabled_plugins = db_group.plugins

  return render_template('pages/group/view.html', group=group, plugins=plugins, enabled_plugins=enabled_plugins)

@pages.route('/groups/<string:group_id>/manage')
@login_required
def manage_group(group_id):
  gat = session['groupme_access_token']

  try:
    group = groupme_api.group(group_id, gat)
  except:
    return redirect(url_for('pages.groups_overview'))

  db_group = Group.query.filter_by(groupme_id=group_id).first()

  if db_group is None:
    return redirect(url_for('pages.group', group_id=group_id))

  if db_group.owner is not g.user:
    return redirect(url_for('pages.view_group'), group_id=group_id)

  plugins = Plugin.query.all()
  enabled_plugins = db_group.plugins

  return render_template('pages/group/manage.html', group=group, plugins=plugins, enabled_plugins=enabled_plugins)

@pages.route('/groups/<string:group_id>/remove')
@login_required
def remove_group(group_id):
  gat = session['groupme_access_token']

  try:
    group = groupme_api.group(group_id, gat)
  except:
    return redirect(url_for('pages.groups_overview'))

  db_group = Group.query.filter_by(groupme_id=group_id, owner=g.user).first()

  if db_group is not None:
    bot_id = db_group.bot_id
    membership_id = get_membership_id(group, groupme_api.me_data['id'])
    remove_lyra_from_group(group_id, gat, bot_id, membership_id)
    db_group.delete()

  return redirect(url_for('pages.groups_overview'))

@pages.route('/groups/<string:group_id>/update', methods=['POST'])
@login_required
def update_group(group_id):
  gat = session['groupme_access_token']

  try:
    groupme_api.group(group_id, gat)
  except:
    return redirect(url_for('pages.groups_overview'))

  db_group = Group.query.filter_by(groupme_id=group_id, owner=g.user).first()

  enabled_plugins_string = list(map(lambda plugin: plugin.name, db_group.plugins))

  for plugin in db_group.plugins:
    if plugin.name not in request.form:
      db_group.plugins.remove(plugin)

  for plugin in request.form:
    if plugin not in enabled_plugins_string:
      db_plugin = Plugin.query.filter_by(name=plugin).first()

      if db_plugin is not None and not db_plugin.disabled:
        db_group.plugins.append(db_plugin)

  db_group.save()

  return redirect(url_for('pages.manage_group', group_id=group_id))

@pages.route('/groups/new/more')
@login_required
def get_more_groups():
  gat = session['groupme_access_token']

  page = request.args['page']

  groups = groupme_api.groups(gat, page=page)

  return render_template('pages/_more.html', groups=groups)
