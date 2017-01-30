#File: tensorflow-db.py
#Authors: Alex Greene & Giancarlo Tarantino

from gamescout_db import db, cur

debug_flag = False

def commit_to_db():
   if debug_flag == False:
      db.commit()

def get_game_ids():
   cur.execute("""
      SELECT
         ID
      FROM
         Games
      """)
   ids = cur.fetchall();
   return ids

def is_one_run_game(game_id):
   cur.execute("""
      SELECT
         HT_RUNS,
         AT_RUNS
      FROM
         Games
      WHERE
         ID = %s  
   """, game_id)

   score = cur.fetchall()
   home = score[0][0]
   away = score[0][1]

   if (home - away) == 1 or (home - away) == -1:
      return True
   else:
      return False

def fill_tensorflow():
   game_ids = get_game_ids()

   for game_id in game_ids:
      one_run = is_one_run_game(game_id)

      cur.execute("""
         INSERT into GamePrediction (
            ID,
            ONE_RUN_GAME
         ) VALUES (%s, %s)
      """,
      [
         game_id,
         one_run
      ])
      commit_to_db()

fill_tensorflow()
