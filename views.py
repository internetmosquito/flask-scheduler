__author__ = 'mosquito'
from flask import Flask, flash, redirect, render_template, request, session, url_for, g
from functools import wraps
from time import localtime, strftime
from forms import AddAppointmentForm
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# import the model
from models import Appointment

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
        return redirect(url_for('login'))
    return wrap

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('You are logged out. Bye. :(')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] \
           or request.form['password'] !=app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
            return render_template('login.html', error=error)
        else:
            session['logged_in'] = True
            return redirect(url_for('appointments'))
    if request.method == 'GET':
        return render_template('login.html')

@app.route('/appointments/')
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
    form = AddAppointmentForm(request.form), future_appointments=future_appointments, past_appointments=past_appointments)

# Adds new appointments:
@app.route('/add/', methods=['POST'])
@login_required
def new_appointment():
    form = AddAppointmentForm(request.form)
    if request.method == 'POST':
        if form.validate():
            if form.validate_on_submit():
                new_appointment = Appointment(
                    form.name.data,
                    form.due_date.data,
                    form.priority.data
                )
                db.session.add(new_appointment)
                db.session.commit()
                flash('New entry was successfully posted. Thanks.')
        else:
            flash('Provided appointment data is invalid, try again')
    return redirect(url_for('appointments'))

# Delete Appointments:
@app.route('/delete/<int:appointment_id>/')
@login_required
def delete_entry(appointment_id):
    apo_id = appointment_id
    db.session.query(Appointment).filter_by(appointment_id=apo_id).delete()
    db.session.commit()
    flash('The appointment was deleted.')
    return redirect(url_for('appointments'))