__author__ = 'mosquito'
import os

# grabs the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'scheduler.db'

# avoid cross site attacks
WTF_CSRF_ENABLED = True
SECRET_KEY = 'super_secret_password'

# defines the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# the database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH