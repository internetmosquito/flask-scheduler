__author__ = 'mosquito'
from flask_wtf import Form
from wtforms import TextField, DateTimeField, IntegerField, SelectField
from wtforms.validators import DataRequired

class AddAppointmentForm(Form):
    appointment_id = IntegerField('Priority')
    name = TextField('Appointment Name', validators=[DataRequired()])
    due_date = DateTimeField('Date Due (YYYY-mm-dd HH:MM:ss)', validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    priority = SelectField('Priority', validators=[DataRequired()], choices=[
                                            ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5','5'),
                                            ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10','10')])
