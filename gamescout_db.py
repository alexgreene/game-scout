# File: mlb_db.py
# Authors: Alex Greene & Giancarlo Tarantino

import MySQLdb
from config import config

# Connect to the database and setup the db cursor.
db = MySQLdb.connect(host = "localhost",
                     user = "root",
                     passwd = config['password'],
                     db = "mlbdata")
cur = db.cursor()
