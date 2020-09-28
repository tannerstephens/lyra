from enum import unique
from flask_sqlalchemy import model
from .extensions import db

Column = db.Column
relationship = db.relationship

class Model(db.Model):
  __abstract__ = True
  id = Column(db.Integer, primary_key=True)

  def save(self, commit=True):
    db.session.add(self)
    if commit:
      db.session.commit()
    return self

class User(Model):
  groupme_id = Column(db.Integer, unique=True, nullable=False)
  groups = relationship('Group', backref='owner', lazy=True)


class Group(Model):
  groupme_id = Column(db.Integer, unique=True, nullable=False)
  user_id = Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
