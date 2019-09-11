from flask import Blueprint
from lyra.models import Group

api = Blueprint('api', __name__)

@api.route('/api/<api_id>')
def process(api_id):
  group = Group.query.filter_by(api_id=api_id).first()

  if not group:
    return ''

  
