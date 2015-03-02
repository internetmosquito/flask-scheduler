__author__ = 'mosquito'
from flask import Flask, flash, redirect, render_template, request, session, url_for, g
from functools import wraps
from time import localtime, strftime
from forms import AddAppointmentForm, RegisterForm, LoginForm
from flask.ext.sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# import the model
from models import Appointment, User

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
    session.pop('user_id', None)
    flash('You are logged out. Bye. :(')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            if form.validate_on_submit():
                u = User.query.filter_by(
                    name=request.form['name'],
                    password=request.form['password']
                    ).first()
                if u is None:
                    error = 'Could not find any user with provided user name or password.'
                    return render_template("login.html", form=form, error=error)
                else:
                    session['logged_in'] = True
                    session['user_id'] = u.id
                    flash('You are logged in. Schedule like mad!.')
                    return redirect(url_for('appointments'))
        else:
            error = 'Provided data is invalid. ' + str(form.errors)
            return render_template("login.html", form=form, error=error)
    if request.method == 'GET':
        return render_template('login.html', form=form)

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
        form = AddAppointmentForm(request.form),
        future_appointments=future_appointments,
        past_appointments=past_appointments)

# Adds new appointments:
@app.route('/add/', methods=['POST'])
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
            error = 'Provided appointment data is invalid. ' + str(form.errors)
            return render_template("appointments.html", error=error)
    return redirect(url_for('appointments'))

# Delete Appointments
@app.route('/delete/<int:appointment_id>/')
@login_required
def delete_entry(appointment_id):
    apo_id = appointment_id
    db.session.query(Appointment).filter_by(appointment_id=apo_id).delete()
    db.session.commit()
    flash('The appointment was deleted.')
    return redirect(url_for('appointments'))

# User Registration:
@app.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate():
            if form.validate_on_submit():
                new_user = User(
                    form.name.data,
                    form.email.data,
                    form.password.data,
                )
                db.session.add(new_user)
                db.session.commit()
                flash('New user created successfully. Please login.')
                return redirect(url_for('login'))
            else:
                return render_template('register.html', form=form, error=error)
        else:
            error = 'Provided data is not valid. More info:' + str(form.errors)
            return render_template('register.html', form=form, error=error)
    if request.method == 'GET':
        return render_template('register.html', form=form)