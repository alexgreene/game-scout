import mlbgame as mlb
import MySQLdb
from config import config
import datetime
#import time

# Connect to the database and setup the db cursor.
db = MySQLdb.connect(host = "localhost",
                     user = "root",
                     passwd = config['password'],
                     db = "mlbdata")
cur = db.cursor()

# for each game
    # add game to GAMES table, with an id as primary key
    # for each game, check if 


#we need to have dates on most of the tables
#how do we get the past five games of a player? make our own i_d?


def fill_db_with_past_games():
    for year in range(2016, 2017):
        for month in range(4, 5):
            for day in range(1, 2):
                game_date = datetime.date(year, month, day).isoformat();
                #game_date = '{}/{}/{}'.format(month, day, year)
                #game_date = datetime.datetime(year, month, day).strftime('%Y-%m-%d')
                print(game_date)

fill_db_with_past_games()
