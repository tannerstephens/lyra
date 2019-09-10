from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(current_app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  groupme_id = db.Column(db.Integer, unique=True)
  image_url = db.column(db.String(500))

