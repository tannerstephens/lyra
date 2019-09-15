from flask import Blueprint, session, current_app, request
from flask_restful import Api, Resource
from .utils import success_message
from .error_messages import *
from lyra.lib.groupme import GroupmeApi

auth_api = Blueprint('auth_api', __name__)
api = Api(auth_api)


class Login(Resource):
  def get(self):
    client_id = current_app.config.get('GROUPME_CLIENT_ID')
    url = 'https://oauth.groupme.com/oauth/authorize?client_id={}'.format(client_id)

    return success_message(True, url=url)


class Callback(Resource):
  def get(self):
    access_token = request.args.get('access_token')

    if access_token:
      session['access_token'] = access_token

      gapi = GroupmeApi(access_token)

      if gapi.get_current_user():
        return success_message(True)
    
    return success_message(False, error=AUTHENTICATION_ERROR)


class Logout(Resource):
  def get(self):
    session.clear()

    return success_message(True)


api.add_resource(Login, '/login')
api.add_resource(Callback, '/callback')
api.add_resource(Logout, '/logout')