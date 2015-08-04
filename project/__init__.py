__author__ = 'mosquito'
import datetime
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_pyfile('_config.py')
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from project.users.views import users_blueprint
from project.appointments.views import appointments_blueprint
from project.api.views import api_blueprint
from flask import render_template

# register our blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(appointments_blueprint)
app.register_blueprint(api_blueprint)

# Define views for errors
@app.errorhandler(404)
def not_found(error):
    if app.debug is not True:
        now = datetime.datetime.now()
        r = request.url
        with open('error.log', 'a') as f:
            current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
            f.write("\n404 error at {}: {}"
                    .format(current_timestamp, r))
    return render_template('error_404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if app.debug is not True:
        now = datetime.datetime.now()
        r = request.url
        with open('error.log', 'a') as f:
            current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
            f.write("\n500 error at {}: {}"
                    .format(current_timestamp, r))
    return render_template('error_500.html'), 500