from flask import Blueprint, redirect, request, session, url_for

def register_blueprint(app, callback_redirect):
  blueprint = Blueprint('groupme_oauth', __name__, url_prefix='/groupme')

  @blueprint.route('/login')
  def login():
    client_id = app.config.get('GROUPME_CLIENT_ID')
    redirect_url = f'https://oauth.groupme.com/oauth/authorize?client_id={client_id}'

    return redirect(redirect_url)

  @blueprint.route('/callback')
  def callback():
    access_token = request.args.get('access_token')
    session['groupme_access_token'] = access_token

    return redirect(url_for(callback_redirect))

  app.register_blueprint(blueprint)
