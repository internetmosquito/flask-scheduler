__author__ = 'mosquito'
from views import db
from models import Appointment
from datetime import datetime

# create the database and the db table
db.create_all()

# insert data
#db.session.add(Appointment("Go to dentist", datetime(2015, 2, 15, 10, 45, 33), 5))
#db.session.add(Appointment("Take car to garage", datetime(2015, 2, 27, 19, 00, 00), 2))
#db.session.add(Appointment("Behold cat world domination", datetime(2015, 3, 2, 12, 00, 00), 10))

# commit the changes
db.session.commit()
