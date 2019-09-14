from flask import Blueprint, session, request
from flask_restful import Api, Resource
from .groupme import GroupmeApi

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)


class CurrentUser(Resource):
  def get(self):
    access_token = session.get('access_token')

    resp = {'logged_in' : False}

    if access_token:
      gapi = GroupmeApi(access_token)

      current_user = gapi.get_current_user()

      if current_user:
        resp['logged_in'] = True

        resp.update(current_user)

    return resp

api.add_resource(CurrentUser, '/current_user')
