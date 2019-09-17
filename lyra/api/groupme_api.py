from flask import Blueprint, session, request
from flask_restful import Api, Resource
from lyra.lib.groupme import GroupmeApi
from lyra.models import Group as GroupDB, db
from .utils import success_message
from .error_messages import *
from uuid import uuid4

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

      page = int(request.args.get('page', 1))

      groups = gapi.get_groups(page)

      if page > 1:
        previous_page = page-1
      else:
        previous_page = False

      if len(groups) < 10 or not len(gapi.get_groups(page + 1)):
        next_page = False
      else:
        next_page = page + 1

      return success_message(True, groups=groups, previous_page=previous_page, next_page=next_page)


    return success_message(False, error=NOT_LOGGED_IN)


class Group(Resource):
  def get(self, group_id):
    access_token = session.get('access_token')

    if access_token:
      gapi = GroupmeApi(access_token)

      group = gapi.get_group(group_id)

      if group:
        groupme_id = group.get('id')
        print(Group)
        db_group = GroupDB.query.filter_by(groupme_id=group_id).first()

        if db_group:
          return success_message(True, group=group, managed=db_group.managed)
        else:
          return success_message(True, group=group, managed=False)

    return success_message(False, error=NOT_LOGGED_IN)

  def post(self, group_id):
    manage = request.json.get('manage')

    if manage is None:
      return success_message(False, error=MANAGE_NOT_PRESENT)

    access_token = session.get('access_token')

    if access_token:
      gapi = GroupmeApi(access_token)

      group = gapi.get_group(group_id)

      if group:
        groupme_id = group.get('id')

        db_group = GroupDB.query.filter_by(groupme_id=group_id).first()

        if not db_group:
          db_group = GroupDB(
            groupme_id = groupme_id,
            api_id = str(uuid4()),
          )

        db_group.managed = manage

        db.session.add(db_group)
        db.session.commit()

        return success_message(True, group=group, managed=db_group.managed)

    return success_message(False, error=NOT_LOGGED_IN)



api.add_resource(CurrentUser, '/current-user')
api.add_resource(Groups, '/groups')
api.add_resource(Group, '/groups/<int:group_id>')
