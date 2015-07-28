__author__ = 'mosquito'
import os
import unittest

from project import app, db, bcrypt
from project._config import basedir
from project.models import Appointment, User


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
        response = self.app.post(
            '/',
            data=dict(
                name=name,
                password=password
            ),
            follow_redirects=True
        )
        #print (response.data)
        return response

    def create_user(self, name=None, email=None, password=None):
        new_user = User(
            name=name,
            email=email,
            password=bcrypt.generate_password_hash(password),
            role='user',
        )
        db.session.add(new_user)
        db.session.commit()

    def create_admin_user(self, name, email, password):
        new_user = User(
            name=name,
            email=email,
            password=bcrypt.generate_password_hash(password),
            role='admin'
        )
        db.session.add(new_user)
        db.session.commit()

    def register(self, name=None, email=None, password=None, confirm=None, role=None):
        return self.app.post(
            'register/',
            data=dict(
                name=name,
                email=email,
                password=password,
                confirm=confirm,
                role=role,
            ),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get('logout/', follow_redirects=True)

    def create_appointment(self, name=None, due_date=None, priority=None, creation_date=None, follow_redirects=None):
        return self.app.post('add/', data=dict(
            name=name,
            due_date=due_date,
            priority=priority,
            creaion_date=creation_date
        ),  follow_redirects=follow_redirects)

    ###############
    #### views ####
    ###############
    def test_logged_in_users_can_access_appointments_page(self):
        self.create_user('JudasPriest', 'judaspriest@isthebest.com', 'judaspriest')
        self.login('JudasPriest', 'judaspriest')
        response = self.app.get('appointments/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn('Add a new appointment:', response.data)

    def test_not_logged_in_users_cannot_access_appointments_page(self):
        response = self.app.get('appointments/', follow_redirects=True)
        self.assertIn('You need to login first.', response.data)

    def test_appointment_template_displays_logged_in_user_name(self):
        self.register('JudasPriest', 'judaspriest@isthebest.com', 'judaspriest', 'judaspriest', 'user')
        self.login('JudasPriest', 'judaspriest')
        response = self.app.get('appointments/', follow_redirects=True)
        self.assertIn(b'JudasPriest', response.data)

    def test_users_cannot_see_appointment_modify_links_for_appointments_not_created_by_them(self):
        self.register('JudasPriest', 'judaspriest@isthebest.com', 'judaspriest', 'judaspriest', 'user')
        self.login('JudasPriest', 'judaspriest')
        self.app.get('appointments/', follow_redirects=True)
        self.create_appointment('Feed the cat', '2015-03-07 09:00:00', priority='1', creation_date='2015-02-07 09:00:00', follow_redirects=True)
        self.logout()
        self.register('MisterWhiteMan', 'mrpresident@whitehouse.com', 'president', 'president', 'user')
        response = self.login('MisterWhiteMan', 'president')
        self.app.get('appointments/', follow_redirects=True)
        #print (response.data)
        self.assertNotIn(b'Delete', response.data)

    def test_users_can_see_appointment_modify_links_for_appointments_created_by_them(self):
        self.register('JudasPriest', 'judaspriest@isthebest.com', 'judaspriest', 'judaspriest', 'user')
        self.login('JudasPriest', 'judaspriest')
        self.app.get('appointments/', follow_redirects=True)
        self.create_appointment('Feed the cat', '2015-03-07 09:00:00', priority='1', creation_date='2015-02-07 09:00:00', follow_redirects=True)
        self.logout()
        self.register('MisterWhiteMan', 'mrpresident@whitehouse.com', 'president', 'president', 'user')
        self.login('MisterWhiteMan', 'president')
        self.app.get('appointments/', follow_redirects=True)
        response = self.create_appointment('Behold cat world domination', '2015-10-25 11:00:00', priority='1', creation_date='2015-08-01 12:18:00', follow_redirects=True)
        #print (response.data)
        self.assertIn(b'delete/2/', response.data)

    def test_admin_users_can_see_appointment_modify_links_for_all_appointments(self):
        self.register('JudasPriest', 'judaspriest@isthebest.com', 'judaspriest', 'judaspriest', 'user')
        self.login('JudasPriest', 'judaspriest')
        self.app.get('appointments/', follow_redirects=True)
        response = self.create_appointment('Feed the cat', '2015-03-07 09:00:00', priority='1', creation_date='2015-02-07 09:00:00', follow_redirects=True)
        #print (response.data)
        self.logout()
        self.create_admin_user('Superman', 'superman@marvel.com', 'allpowerful')
        self.login('Superman', 'allpowerful')
        self.app.get('appointments/', follow_redirects=True)
        response = self.create_appointment('Behold cat world domination', '2015-10-25 11:00:00', priority='1', creation_date='2015-08-01 12:18:00', follow_redirects=True)
        #print (response.data)
        self.assertIn(b'delete/1/', response.data)
        self.assertIn(b'delete/2/', response.data)

    ###############
    #### forms ####
    ###############
    def test_users_can_add_appointments(self):
        self.create_user('JudasPriest', 'judaspriest@isthebest.com', 'judaspriest')
        self.login('JudasPriest', 'judaspriest')
        self.app.get('appointments/', follow_redirects=True)
        response = self.create_appointment('Feed the cat', '2015-03-07 09:00:00', priority='1', creation_date='2015-02-07 09:00:00', follow_redirects=True)
        self.assertIn('New entry was successfully posted. Thanks.', response.data)

    def test_users_add_appointment_fail_required_field(self):
        self.create_user('JudasPriest', 'judaspriest@isthebest.com', 'judaspriest')
        self.login('JudasPriest', 'judaspriest')
        self.app.get('appointments/', follow_redirects=True)
        response = self.app.post('add/', data=dict(
            name='Behold cat domination',
            due_date='',
            priority='1',
            creation_date='2015-02-07 09:00:00'
        ),  follow_redirects=True)
        self.assertIn('This field is required.', response.data)

    def test_users_can_delete_appointments(self):
        self.create_user('JudasPriest', 'judaspriest@isthebest.com', 'judaspriest')
        self.login('JudasPriest', 'judaspriest')
        self.app.get('appointments/', follow_redirects=True)
        self.create_appointment('Feed the cat', '2015-03-07 09:00:00', priority='1', creation_date='2015-02-07 09:00:00', follow_redirects=True)
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertIn('The appointment was deleted successfully', response.data)

    def test_users_cannot_delete_appointments_that_are_not_created_by_them(self):
        self.create_user('JudasPriest', 'judaspriest@isthebest.com', 'judaspriest')
        self.login('JudasPriest', 'judaspriest')
        self.app.get('appointments/', follow_redirects=True)
        self.create_appointment('Feed the cat', '2015-03-07 09:00:00', priority='1', creation_date='2015-02-07 09:00:00', follow_redirects=True)
        self.logout()
        self.register('MisterWhiteMan', 'mrpresident@whitehouse.com', 'president', 'president', 'user')
        self.login('MisterWhiteMan', 'president')
        self.app.get('appointments/', follow_redirects=True)
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertIn(
            'You can only delete appointments that you have created',
            response.data
        )

    def test_admin_users_can_delete_appointments_that_are_not_created_by_them(self):
        self.create_user('JudasPriest', 'judaspriest@isthebest.com', 'judaspriest')
        self.login('JudasPriest', 'judaspriest')
        self.app.get('appointments/', follow_redirects=True)
        self.create_appointment('Feed the cat', '2015-03-07 09:00:00', priority='1', creation_date='2015-02-07 09:00:00', follow_redirects=True)
        self.logout()
        self.create_admin_user('Superman', 'superman@marvel.com', 'allpowerful')
        self.login('Superman', 'allpowerful')
        self.app.get('appointments/', follow_redirects=True)
        response = self.app.get("delete/1/", follow_redirects=True)
        #print (response.data)
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
        #print appointments
        for appointment in appointments:
            self.assertEquals(appointment.name, 'Just a test')


if __name__ == "__main__":
    unittest.main()
