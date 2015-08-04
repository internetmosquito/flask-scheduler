__author__ = 'mosquito'
import os
import unittest
import datetime

from project import app, db
from project._config import basedir
from project.models import Appointment

TEST_DB = 'test.db'


class APITests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()
        self.assertEquals(app.debug, False)

    # executed after to each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ########################
    #### helper methods ####
    ########################

    def add_appointments(self):
        new_appointment = Appointment(
            'Conquer the world',
            datetime.datetime(2017, 10, 22),
            1,
            datetime.datetime.utcnow(),
            1
        )
        db.session.add(new_appointment)
        db.session.commit()
        new_appointment = Appointment(
            'Become a Jedi',
            datetime.datetime(2016, 5, 11),
            1,
            datetime.datetime.utcnow(),
            1
        )
        db.session.add(new_appointment)
        db.session.commit()

    ###############
    #### tests ####
    ###############

    def test_collection_endpoint_returns_correct_data(self):
        self.add_appointments()
        response = self.app.get('api/v1/appointments/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertIn(b'Conquer the world', response.data)
        self.assertIn(b'Become a Jedi', response.data)

    def test_resource_endpoint_returns_correct_data(self):
        self.add_appointments()
        response = self.app.get('api/v1/appointments/2', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertIn(b'Become a Jedi', response.data)
        self.assertNotIn(b'Conquer the world', response.data)

    def test_invalid_resource_endpoint_returns_error(self):
        self.add_appointments()
        response = self.app.get('api/v1/appointments/999',
                                follow_redirects=True)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertIn(b'Specified appointment does not exist', response.data)

    if __name__ == "__main__":
        unittest.main()