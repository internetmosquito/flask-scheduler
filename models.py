__author__ = 'mosquito'
from views import db
import datetime

class Appointment(db.Model):

    __tablename__ = "appointments"

    appointment_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, due_date, priority, creation_time, user_id):
        self.name = name
        self.due_date = due_date
        self.priority = priority
        self.creation_date = creation_time
        self.user_id = user_id

    def __repr__(self):
        return '<name %r>' % (self.name)


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    appointments = db.relationship('Appointment', backref='poster')
    role = db.Column(db.String, default='user')
    permissions = db.Column(db.String, default='normal')

    def __init__(self, name=None, email=None, password=None, role=None):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return '<User %r>' % (self.name)