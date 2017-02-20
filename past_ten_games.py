from gamescout_db import db, cur
import tensorflow_db as tf

def past_10_games(team, g_date):
   cur.execute("""
      SELECT
         ID
      FROM
         GAMES
      WHERE
         (HT = %s OR AT = %s)
      AND G_DATE < %s
      ORDER BY G_DATE DESC
      LIMIT 10
   """, [team, team, g_date])
   row = cur.fetchall()

   return row

def past_ten():
   game_ids = tf.get_game_ids()

   count = 1

   for game_id in game_ids:   
      game = tf.get_game(game_id)
      
      ht = past_10_games(game['HT'], game['G_DATE'])
      at = past_10_games(game['AT'], game['G_DATE'])

      #Inserting past 10 for home team
      for g in ht:
         cur.execute("""
            INSERT into PastTenGames (
               G_ID,
               PAST_GAME,
               IS_HOME
            ) VALUES (%s,%s,%s)
         """, [
            game_id[0],
            g[0],
            '1'
         ])
         db.commit()

      #Inserting past 10 for away team
      for g in at: 
         cur.execute("""
            INSERT into PastTenGames (
               G_ID,
               PAST_GAME,
               IS_HOME
            ) VALUES (%s,%s,%s)
         """, [
            game_id[0],
            g[0],
            '0'
         ])
         db.commit()

      print("Cnt: " + str(count) + " G_ID: " + game_id[0])
      count += 1

if __name__ == '__main__':
   past_ten()
