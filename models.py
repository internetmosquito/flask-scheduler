__author__ = 'mosquito'
from views import db

class Appointment(db.Model):

    __tablename__ = "appointments"

    appointment_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.Integer, nullable=False)

    def __init__(self, name, due_date, priority):
        self.name = name
        self.due_date = due_date
        self.priority = priority

    def __repr__(self):
        return '<name %r>' % (self.name)