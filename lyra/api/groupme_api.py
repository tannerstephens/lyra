from flask import Blueprint, session, request
from flask_restful import Api, Resource
from lyra.lib.groupme import GroupmeApi
from .utils import success_message
from .error_messages import *

groupme_api = Blueprint('groupme_api', __name__)
api = Api(groupme_api)


class CurrentUser(Resource):
  def get(self):
    access_token = session.get('access_token')

    if access_token:
      gapi = GroupmeApi(access_token)

      current_user = gapi.get_current_user()

      if current_user:
        return success_message(True, currentUser=current_user)
      else:
        session.clear()

    return success_message(False, error=NOT_LOGGED_IN)


class Groups(Resource):
  def get(self):
    access_token = session.get('access_token')



api.add_resource(CurrentUser, '/current_user')
