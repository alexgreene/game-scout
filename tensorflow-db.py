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

def get_game(game_id):
   cur.execute("""
      SELECT
         *
      FROM
         Games
      WHERE
         ID = %s
   """, game_id)

   row = cur.fetchall()
   return create_game_obj(row[0])


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

def is_two_run_game(game_id):
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

   if (home - away) == 2 or (home - away) == -2:
      return True
   else:
      return False

#Builds a game object from a single row
def create_game_obj(row):
   game = {}
   game['G_DATE'] = row[0]
   game['G_TYPE'] = row[1]
   game['ID'] = row[2]
   game['LEAGUE'] = row[3]
   game['STATUS'] = row[4]
   game['START_TIME'] = row[5]
   game['HT'] = row[6]
   game['HT_RUNS'] = row[7]
   game['HT_HITS'] = row[8]
   game['HT_ERRORS'] = row[9]
   game['AT'] = row[10]
   game['AT_RUNS'] = row[11]
   game['AT_HITS'] = row[12]
   game['AT_ERRORS'] = row[13]
   game['W_PITCHER'] = row[14]
   game['W_PITCHER_WINS'] = row[15]
   game['W_PITCHER_LOSSES'] = row[16]
   game['L_PITCHER'] = row[17]
   game['L_PITCHER_WINS'] = row[18]
   game['L_PITCHER_LOSSES'] = row[19]
   game['SV_PITCHER'] = row[20]
   game['SV_PITCHER_SAVES'] = row[21]
   
   return game

#Gets the win pct of a team up until the given date
def get_win_pct(team, date):
   cur.execute("""
      SELECT
         *
      FROM
         Games
      Where
         (HT = %s or AT = %s)
         AND G_DATE < %s
         AND YEAR(G_DATE) = %s
   """, [team, team, date, str(date.year)])

   games = cur.fetchall()

   totalGames = 0;
   wins = 0;

   if not games:
      return 0
   else:
      for row in games:
         game = create_game_obj(row)

         if game['HT'] == team:
            if game['HT_RUNS'] > game['AT_RUNS']:
               wins += 1
         else:
            if game['AT_RUNS'] > game['HT_RUNS']:
               wins += 1
            
         totalGames += 1

      return round(float(wins)/float(totalGames), 3)

#Gets the absolute value of the diff in win % for two teams
def diff_in_win_pct(game_id):
   cur.execute("""
      SELECT
         *
      FROM
         Games
      WHERE
         ID = %s
   """, game_id)

   row = cur.fetchall()
   game = create_game_obj(row[0])

   home_pct = get_win_pct(game['HT'], game['G_DATE'])
   away_pct = get_win_pct(game['AT'], game['G_DATE'])

   return abs(home_pct - away_pct)

def get_run_diff(team, date):
   cur.execute("""
      SELECT
         *
      FROM
         Games
      Where
         (HT = %s or AT = %s)
         AND G_DATE < %s
         AND YEAR(G_DATE) = %s
   """, [team, team, date, str(date.year)])

   games = cur.fetchall()

   runs_scored = 0;
   runs_allowed = 0;

   if not games:
      return 0
   else:
      for row in games:
         game = create_game_obj(row)

         if game['HT'] == team:
            runs_scored += game['HT_RUNS']
            runs_allowed += game['AT_RUNS']
         else:
            runs_scored += game['AT_RUNS']
            runs_allowed += game['HT_RUNS']
            
      return runs_scored - runs_allowed
   
def get_run_differentials(game_id):
   cur.execute("""
      SELECT
         *
      FROM
         Games
      WHERE
         ID = %s
   """, game_id)

   row = cur.fetchall()
   game = create_game_obj(row[0])

   home_diff = get_run_diff(game['HT'], game['G_DATE'])
   away_diff = get_run_diff(game['AT'], game['G_DATE'])
   diff_in_run_diffs = abs(home_diff - away_diff)

   return (home_diff, away_diff, diff_in_run_diffs)

#Main function to fill tensorflow db table
def fill_tensorflow():
   game_ids = get_game_ids()

   for game_id in game_ids:
      one_run_game = is_one_run_game(game_id)
      two_run_game = is_two_run_game(game_id)
      run_diffs = get_run_differentials(game_id)
      
      if one_run_game:
         game = get_game(game_id)
         ht_wpct_one_run = get_win_pct(game['HT'], game['G_DATE'])
         at_wpct_one_run = get_win_pct(game['AT'], game['G_DATE'])
      else:
         ht_wpct_one_run = None
         at_wpct_one_run = None

      if two_run_game:
         game = get_game(game_id)
         ht_wpct_two_run = get_win_pct(game['HT'], game['G_DATE'])
         at_wpct_two_run = get_win_pct(game['AT'], game['G_DATE'])
      else:
         ht_wpct_two_run = None
         at_wpct_two_run = None

      cur.execute("""
         INSERT into GamePrediction (
            ID,
            ONE_RUN_GAME,
            DIFF_IN_WPCT,
            HT_WPCT_1RUN,
            AT_WPCT_1RUN,
            HT_WPCT_2RUN,
            AT_WPCT_2RUN,
            RUN_DIFF_HT,
            RUN_DIFF_AT,
            DIFF_IN_RUN_DIFF
         ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
      """,
      [
         game_id,
         one_run_game,
         diff_in_win_pct(game_id),
         ht_wpct_one_run,
         at_wpct_one_run,
         ht_wpct_two_run,
         at_wpct_two_run,
         run_diffs[0],
         run_diffs[1],
         run_diffs[2]         
      ])
      commit_to_db()

fill_tensorflow()
