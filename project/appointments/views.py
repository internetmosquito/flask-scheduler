__author__ = 'mosquito'

#################
#### imports ####
#################

from functools import wraps
from flask import flash, redirect, render_template, \
    request, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError
import datetime
from time import localtime, strftime

from project.appointments.forms import AddAppointmentForm
from project import db
from project.models import Appointment


################
#### config ####
################

appointments_blueprint = Blueprint('appointments', __name__)

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

@appointments_blueprint.route('/appointments/')
@login_required
def appointments():
    # Get current date
    current_datetime = strftime("%Y-%m-%d %H:%M:%S", localtime())
    future_appointments = db.session.query(Appointment)\
        .filter(Appointment.due_date >= current_datetime)\
        .order_by(Appointment.due_date.asc())
    past_appointments = db.session.query(Appointment)\
        .filter(Appointment.due_date < current_datetime)\
        .order_by(Appointment.due_date.asc())
    return render_template('appointments.html',
        form = AddAppointmentForm(request.form),
        future_appointments=future_appointments,
        past_appointments=past_appointments)

@appointments_blueprint.route('/add/', methods=['GET', 'POST'])
@login_required
def new_appointment():
    error = None
    form = AddAppointmentForm(request.form)
    if request.method == 'POST':
        if form.validate():
            if form.validate_on_submit():
                new_appointment = Appointment(
                    form.name.data,
                    form.due_date.data,
                    form.priority.data,
                    datetime.datetime.utcnow(),
                    session['user_id']
                )
                db.session.add(new_appointment)
                db.session.commit()
                flash('New entry was successfully posted. Thanks.')
        else:
            return render_template("appointments.html", form=form)
    return redirect(url_for('appointments.appointments'))


@appointments_blueprint.route('/delete/<int:appointment_id>/')
@login_required
def delete_entry(appointment_id):
    apo_id = appointment_id
    appointment = db.session.query(Appointment).filter_by(appointment_id=apo_id)
    if session['user_id'] == appointment.first().user_id or session['role'] == "admin":
        appointment.delete()
        db.session.commit()
        flash('The appointment was deleted successfully')
        return redirect(url_for('appointments.appointments'))
    else:
        flash('You can only delete appointments that you have created')
        return redirect(url_for('appointments.appointments'))