from logging import getLogger

from flask import Flask
from flask_migrate import upgrade

from .before_request import before_request
from .extensions import db, groupme_api, groupme_oauth, migrate
from .lyra_bot import lyra
from .models import Group, User
from .routes import register_blueprints


def create_app(config='lyra.config.Config'):
  app = Flask(__name__)
  app.config.from_object(config)

  with app.app_context():
    register_extensions(app)
    register_blueprints(app)
    before_request(app)
    lyra.init_app(app)
    register_groups(app)

  return app

def register_extensions(app):
  db.init_app(app)
  migrate.init_app(app, db)
  upgrade()
  groupme_oauth.init_app(app, 'auth.login')
  groupme_api.init_app(app)

def register_logger(app):
  gunicorn_logger = getLogger('gunicorn.error')
  app.loggers.handlers = gunicorn_logger.handlers

def register_groups(app):
  bots = {bot['group_id']: bot['bot_id'] for bot in groupme_api.list_bots()}

  for groupme_group in groupme_api.all_groups(omit_members=False):
    group_id = groupme_group['group_id']
    group = Group.query.filter_by(groupme_id=group_id).first()

    if group is None:
      owner = filter(lambda member: 'owner' in member['roles'], groupme_group['members']).__next__()
      owner_user = User.query.filter_by(groupme_id=owner['user_id']).first()

      if owner_user is None:
        owner_user = User(groupme_id=owner['user_id']).save()

      bot_id = bots.get(group_id)

      if bot_id is None:
        callback = callback = app.config['BASE_URL'] + '/lyra/'
        bot = groupme_api.create_bot(group_id, 'Lyra Listener', callback)
        bot_id = bot['bot']['bot_id']

      group = Group(
        groupme_id=group_id,
        owner=owner_user,
        bot_id=bot_id
      ).save()



app = create_app()
