__author__ = 'mosquito'
from flask import Flask, flash, redirect, render_template, request, session, url_for, g
from functools import wraps
import sqlite3
from time import localtime, strftime
from forms import AddAppointmentForm

app = Flask(__name__)
app.config.from_object('config')

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

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
    g.db = connect_db()
    # Get current date
    current_datetime = strftime("%Y-%m-%d %H:%M:%S", localtime())
    cur = g.db.execute('select name, due_date, priority, appointment_id from appointments where due_date >= ?', (current_datetime,))
    future_appointments = [dict(name=row[0], due_date=row[1], priority=row[2], appointment_id=row[3]) for row in cur.fetchall()]
    cur = g.db.execute('select name, due_date, priority, appointment_id from appointments where due_date < ?', (current_datetime,))
    past_appointments = [dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3]) for row in cur.fetchall()]
    g.db.close()
    return render_template('appointments.html',
    form = AddAppointmentForm(request.form), future_appointments=future_appointments, past_appointments=past_appointments)

# Adds new appointments:
@app.route('/add/', methods=['POST'])
@login_required
def new_appointment():
    g.db = connect_db()
    name = request.form['name']
    date = request.form['due_date']
    priority = request.form['priority']
    if not name or not date or not priority:
        flash("All fields are required. Please try again.")
        return redirect(url_for('appointments'))
    else:
        g.db.execute('insert into appointments (name, due_date, priority) values (?, ?, ?)',
                    [request.form['name'],
                     request.form['due_date'],
                     request.form['priority']])
    g.db.commit()
    g.db.close()
    flash('New entry was successfully posted. Thanks.')
    return redirect(url_for('appointments'))

# Delete Appointments:
@app.route('/delete/<int:appointment_id>/')
@login_required
def delete_entry(appointment_id):
    g.db = connect_db()
    g.db.execute('delete from appointments where appointment_id='+str(appointment_id))
    g.db.commit()
    g.db.close()
    flash('The appointment was deleted.')
    return redirect(url_for('appointments'))