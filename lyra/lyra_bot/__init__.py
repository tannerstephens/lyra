from glob import glob
from importlib.util import spec_from_file_location, module_from_spec
from os import path

from flask import request
from lyra.extensions import groupme_api
from lyra.models import Group, Plugin

DIR = path.dirname(path.abspath(__file__))

class LyraBot:
  def __init__(self, app=None):
    self.app = app
    if app is not None:
      self.init_app(app)

  def init_app(self, app):
    self._load_plugins()
    self.app = app
    @app.route('/lyra/', methods=['POST'])
    def handle():
      self._handle_message(request.json)
      return ''

  def get_names(self):
    return list(map(lambda plugin: plugin.NAME, self.plugins))

  def _handle_message(self, data):
    if(data['sender_id'] != groupme_api.me_data['id']):
      self.app.logger.info(data)
      self._run_plugins(data)

  def _run_plugins(self, data):
    group = Group.query.filter_by(groupme_id=data['group_id']).first()

    if group is None:
      return

    enabled_plugins = set(map(lambda plugin: plugin.name, group.plugins))

    for plugin in self.plugins:
      if plugin.NAME in enabled_plugins:
        try:
          plugin.handle(data, groupme_api)
        except Exception as e:
          print(f'Exception during handling of {plugin.NAME}')
          print(e)
          print(data)

  def _load_plugins(self):
    self.plugins = []

    for i, plugin_path in enumerate(glob(f'{DIR}/plugins/*.py')):
      spec = spec_from_file_location(f'plugin{i}', plugin_path)
      plugin = module_from_spec(spec)
      spec.loader.exec_module(plugin)
      self.plugins.append(plugin)

      db_plugin = Plugin.query.filter_by(name=plugin.NAME).first()

      if db_plugin is None:
        db_plugin = Plugin(name=plugin.NAME)

      db_plugin.help = plugin.HELP
      try:
        db_plugin.disabled = plugin.DISABLED
      except:
        db_plugin.disabled = False

      db_plugin.save()

lyra = LyraBot()
