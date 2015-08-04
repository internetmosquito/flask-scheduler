__author__ = 'mosquito'
from functools import wraps
from flask import flash, redirect, jsonify, \
    session, url_for, Blueprint, make_response

from project import db
from project.models import Appointment

################
#### config ####
################

api_blueprint = Blueprint('api', __name__)

##########################
#### helper functions ####
##########################


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('users.login'))
    return wrap


def open_appointments():
    return db.session.query(Appointment).filter_by(status='1')\
        .order_by(Appointment.due_date.asc())


def closed_appointments():
    return db.session.query(Appointment).filter_by(status='0')\
        .order_by(Appointment.due_date.asc())

################
#### routes ####
################

@api_blueprint.route('/api/v1/appointments/')
def api_appointments():
    results = db.session.query(Appointment).limit(10).offset(0).all()
    json_results = []
    for result in results:
        data = {
            'appointment_id': result.appointment_id,
            'appointment name': result.name,
            'due date': str(result.due_date),
            'priority': result.priority,
            'creation date': str(result.creation_date),
            'user id': result.user_id
        }
        json_results.append(data)
    return jsonify(items=json_results)

@api_blueprint.route('/api/v1/appointments/<int:appointment_id>')
def appointment(appointment_id):
    result = db.session.query(Appointment).filter_by(appointment_id=appointment_id).first()
    if result:
        json_result = {
            'appointment_id': result.task_id,
            'appointment name': result.name,
            'due date': str(result.due_date),
            'priority': result.priority,
            'posted date': str(result.posted_date),
            'status': result.status,
            'user id': result.user_id
        }
        code = 200
    else:
        result = {"error": "Specified appointment does not exist"}
        code = 404
    return make_response(jsonify(result), code)
