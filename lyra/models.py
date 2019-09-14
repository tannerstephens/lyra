from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(current_app)


class Group(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  groupme_id = db.Column(db.Integer, unique=True)
  aliases = db.relationship('Alias', backref='group', lazy=True)
  api_id = db.Column(db.String(36), unique=True)


class Alias(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  key = db.Column(db.String(50))
  group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
  user_id = db.Column(db.Integer)
