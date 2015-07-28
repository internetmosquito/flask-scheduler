__author__ = 'mosquito'

#################
#### imports ####
#################

from functools import wraps
from flask import flash, redirect, render_template, \
    request, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError

from project.users.forms import RegisterForm, LoginForm
from project import db, bcrypt
from project.models import User

#######################
#### configuration ####
#######################

users_blueprint = Blueprint('users', __name__)

##########################
#### helper_functions ####
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

##########################
#######  routes  #########
##########################

@users_blueprint.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('role', None)
    session.pop('name', None)
    flash('You are logged out. Bye. :(')
    return redirect(url_for('users.login'))

@users_blueprint.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['name']).first()
            if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):
                session['logged_in'] = True
                session['user_id'] = user.id
                session['role'] = user.role
                session['name'] = user.name
                flash('You are logged in. Schedule like mad!')
                return redirect(url_for('appointments.appointments'))
            else:
                error = 'Could not find any user with provided user name or password.'
                return render_template('login.html', form=form, error=error)
    return render_template('login.html', form=form, error=error)

@users_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(
            form.name.data,
            form.email.data,
            bcrypt.generate_password_hash(form.password.data),
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('New user created successfully. Please login.')
                return redirect(url_for('users.login'))
            except IntegrityError:
                error = 'Provided username and password exist already, try again with different values'
                return render_template('register.html', form=form, error=error)
    return render_template('register.html', form=form, error=error)