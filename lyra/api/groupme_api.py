from flask import Blueprint, session, request
from flask_restful import Api, Resource
from lyra.lib.groupme import GroupmeApi
from lyra.models import Group, db
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

    if access_token:
      gapi = GroupmeApi(access_token)

      page = request.args.get('page', 1)

      groups = gapi.get_groups(page)

      return success_message(True, groups=groups)

    
    return success_message(False, error=NOT_LOGGED_IN)


class Group(Resource):
  def get(self, group_id):
    access_token = session.get('access_token')

    if access_token:
      gapi = GroupmeApi(access_token)

      group = gapi.get_group(group_id)

      if group:
        groupme_id = group.get('id')
        db_group = Group.query.filter_by(group_id=group_id).first()

        if db_group:
          managed = True
        else:
          managed = False

        return success_message(True, group=group, managed=managed)
      else:
        return success_message(False, error=GROUPME_NOT_AUTHORIZED)
    
    return success_message(False, error=NOT_LOGGED_IN)


api.add_resource(CurrentUser, '/current-user')
api.add_resource(Groups, '/groups')
api.add_resource(Groups, '/groups/<int:group_id>')
