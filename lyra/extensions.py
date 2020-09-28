from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .groupme_oauth import GroupmeOAuth
from .groupme_api import GroupmeAPI

migrate = Migrate()
db = SQLAlchemy()
groupme_oauth = GroupmeOAuth()
groupme_api = GroupmeAPI()
