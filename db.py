__author__ = 'mosquito'
import sqlite3
from config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:
    # get a cursor object used to execute SQL commands
    c = connection.cursor()

    # create the table
    c.execute("""CREATE TABLE appointments(appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                           name TEXT NOT NULL,
                                           due_date DATETIME NOT NULL,
                                           priority INTEGER NOT NULL)""")

    # insert dummy data into the table
    c.execute('INSERT INTO appointments (name, due_date, priority)'
                'VALUES("Go to dentist", "2015-02-15 10:45:33", 5)')
    c.execute('INSERT INTO appointments (name, due_date, priority)'
                'VALUES("Take car to garage", "2015-02-27 19:22:12", 10)')