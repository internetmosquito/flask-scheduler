__author__ = 'mosquito'
# test_tasks.py


import os
import unittest

from views import app, db
from config import basedir
from models import Appointment, User

TEST_DB = 'test.db'


class AppointmentsTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    # executed after to each test
    def tearDown(self):
        db.drop_all()

    ########################
    #### helper methods ####
    ########################

    def login(self, name, password):
        return self.app.post(
            '/',
            data=dict(
                name=name,
                password=password
            ),
            follow_redirects=True
        )

    def create_user(self):
        new_user = User(
            name='JamboJambo',
            email='theking@ofthejungle.com',
            password='jungleking',
            role='user'
        )
        db.session.add(new_user)
        db.session.commit()

    def create_admin_user(self):
        new_user = User(
            name='Superman',
            email='admin@realpython.com',
            password='allpowerful',
            role='admin'
        )
        db.session.add(new_user)
        db.session.commit()

    def register(self):
        return self.app.post(
            'register/',
            data=dict(
                name='MisterWhiteMan',
                email='misterwhiteman@real.gov',
                password='president',
                confirm='president',
                role='user'
            ),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get('logout/', follow_redirects=True)

    def create_appointment(self):
        return self.app.post('add/', data=dict(
            name='Feed the cat',
            due_date='2015-03-07 09:00:00',
            priority='1',
            creaion_date='2015-02-07 09:00:00'
        ),  follow_redirects=True)

    ###############
    #### views ####
    ###############
    def test_logged_in_users_can_access_appointments_page(self):
        self.create_user()
        self.login('JamboJambo', 'jungleking')
        response = self.app.get('appointments/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn('Add a new appointment:', response.data)

    def test_not_logged_in_users_cannot_access_appointments_page(self):
        response = self.app.get('appointments/', follow_redirects=True)
        self.assertIn('You need to login first.', response.data)

    ###############
    #### forms ####
    ###############
    def test_users_can_add_appointments(self):
        self.create_user()
        self.login('JamboJambo', 'jungleking')
        self.app.get('appointments/', follow_redirects=True)
        response = self.create_appointment()
        self.assertIn('New entry was successfully posted. Thanks.', response.data)

    def test_users_add_appointment_fail_required_field(self):
        self.create_user()
        self.login('JamboJambo', 'jungleking')
        self.app.get('appointments/', follow_redirects=True)
        response = self.app.post('add/', data=dict(
            name='Behold cat domination',
            due_date='',
            priority='1',
            creation_date='2015-02-07 09:00:00'
        ),  follow_redirects=True)
        self.assertIn('This field is required.', response.data)

    def test_users_can_delete_appointments(self):
        self.create_user()
        self.login('JamboJambo', 'jungleking')
        self.app.get('appointments/', follow_redirects=True)
        self.create_appointment()
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertIn('The appointment was deleted successfully', response.data)

    def test_users_cannot_delete_appointments_that_are_not_created_by_them(self):
        self.create_user()
        self.login('JamboJambo', 'jungleking')
        self.app.get('appointments/', follow_redirects=True)
        self.create_appointment()
        self.logout()
        self.register()
        self.login('MisterWhiteMan', 'president')
        self.app.get('appointments/', follow_redirects=True)
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertIn(
            'You can only delete appointments that you have created',
            response.data
        )

    def test_admin_users_can_delete_appointments_that_are_not_created_by_them(self):
        self.create_user()
        self.login('JamboJambo', 'jungleking')
        self.app.get('appointments/', follow_redirects=True)
        self.create_appointment()
        self.logout()
        self.create_admin_user()
        self.login('Superman', 'allpowerful')
        self.app.get('appointments/', follow_redirects=True)
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertNotIn(
            'You can only delete appointments that you have created', response.data
        )

    ################
    #### models ####
    ################

    def test_string_reprsentation_of_the_appointment_object(self):

        from datetime import date
        db.session.add(
            Appointment(
                "Just a test",
                date(2015, 3, 13),
                10,
                date(2015, 2, 14),
                1
            )
        )

        db.session.commit()

        appointments = db.session.query(Appointment).all()
        print appointments
        for appointment in appointments:
            self.assertEquals(appointment.name, 'Just a test')


if __name__ == "__main__":
    unittest.main()
