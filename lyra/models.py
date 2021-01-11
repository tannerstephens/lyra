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

  def delete(self, commit=True):
    db.session.delete(self)
    return commit and db.session.commit()

plugins = db.Table('plugins',
  db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True),
  db.Column('plugin_id', db.Integer, db.ForeignKey('plugin.id'), primary_key=True)
)

class User(Model):
  groupme_id = Column(db.Integer, unique=True, nullable=False)
  groups = relationship('Group', backref='owner', lazy=True)


class Group(Model):
  groupme_id = Column(db.Integer, unique=True, nullable=False)
  bot_id = Column(db.Integer, unique=True, nullable=False)
  user_id = Column(db.String(40), db.ForeignKey('user.id'), nullable=False)
  plugins = relationship('Plugin', secondary=plugins, lazy=True, backref='groups')

class Plugin(Model):
  name = Column(db.String(80), unique=True, nullable=False)
  help = Column(db.String(80))

  def __repr__(self):
    return self.name
