__author__ = 'mosquito'
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('_config.py')
db = SQLAlchemy(app)

from project.users.views import users_blueprint
from project.appointments.views import appointments_blueprint

# register our blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(appointments_blueprint)