from flask import Blueprint

lyra = Blueprint('lyra', __name__, url_prefix='/lyra')

@lyra.route('/')
def listener():
  return ''
