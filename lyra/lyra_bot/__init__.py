from glob import glob
from importlib.util import spec_from_file_location, module_from_spec
from os import path

from flask import request
from lyra.extensions import groupme_api

DIR = path.dirname(path.abspath(__file__))

class LyraBot:
  def __init__(self, app=None):
    self._load_plugins()

    if app is not None:
      self.init_app(app)

  def init_app(self, app):
    @app.route('/lyra/', methods=['POST'])
    def handle():
      self._handle_message(request.json)
      return ''

  def get_names(self):
    return list(map(lambda plugin: plugin.NAME, self.plugins))

  def _handle_message(self, data):
    if(data['sender_id'] != groupme_api.me_data['id']):
      self._run_plugins(data)

  def _run_plugins(self, data):
    for plugin in self.plugins:
      plugin.handle(data)

  def _load_plugins(self):
    self.plugins = []

    for i, plugin_path in enumerate(glob(f'{DIR}/plugins/*.py')):
      spec = spec_from_file_location(f'plugin{i}', plugin_path)
      plugin = module_from_spec(spec)
      spec.loader.exec_module(plugin)
      self.plugins.append(plugin)

lyra = LyraBot()
