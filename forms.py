__author__ = 'mosquito'
from flask_wtf import Form
from wtforms import TextField, DateTimeField, IntegerField, \
SelectField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class AddAppointmentForm(Form):
    appointment_id = IntegerField('Priority')
    name = TextField('Appointment Name', validators=[DataRequired()])
    due_date = DateTimeField('Date Due (YYYY-mm-dd HH:MM:ss)', validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    priority = SelectField('Priority', validators=[DataRequired()], choices=[
                                            ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5','5'),
                                            ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10','10')])

class RegisterForm(Form):
    name = TextField(
        'Username',
        validators=[DataRequired(),
        Length(min=6, max=25)]
    )
    email = TextField(
        'Email',
        validators=[DataRequired(),
        Email(),
        Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(),
        Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password',
        message='Passwords must match')]
    )

class LoginForm(Form):
    name = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password',
        validators=[DataRequired()])