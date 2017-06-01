#File: pitchers.py
#Authors: Alex Greene & Giancarlo Tarantino

from gamescout_db import db, cur
debug_flag = False

def commit_to_db(stmt, data):
   if debug_flag == False:
      cur.executemany(stmt, data)
      db.commit()

def get_pitchers():
   cur.execute("""
      SELECT
         *
      FROM
         PitcherStats
      ORDER BY
         NAME,
         G_DATE ASC
   """)

   row = cur.fetchall()
   return row

def create_pitcher_obj(row):
   p = {}
   p['ID'] = row[0];                      p['G_DATE'] = row[1]
   p['NAME'] = row[2];                    p['NAME_ABBR'] = row[3]
   p['TEAM'] = row[4];                    p['AT_HOME'] = row[5]
   p['POS'] = row[6];                     p['G_ID'] = row[7]
   p['P_ID'] = row[8];                    p['HITS'] = row[9]
   p['RUNS'] = row[10];                   p['HR'] = row[11]
   p['BB'] = row[12];                     p['K'] = row[13]
   p['SEA_HITS'] = row[14];               p['SEA_RUNS'] = row[15]
   p['SEA_RUNS'] = row[16];               p['SEA_BB'] = row[17]
   p['SEA_L'] = row[18];                  p['SEA_W'] = row[19]
   p['SEA_SV'] = row[20];                 p['ER'] = row[21]
   p['HOLD'] = row[22];                   p['BLOWN_SV'] = row[23]
   p['OUTS'] = row[24];                   p['BATTERS_FACED'] = row[25]
   p['GAME_SCORE'] = row[26];             p['ERA'] = row[27]
   p['PITCHES'] = row[28];                p['WIN'] = row[29]
   p['LOSS'] = row[30];                   p['SAVE'] = row[31]
   p['NOTE'] = row[32];                   p['SEA_ER'] = row[33]
   p['SEA_IP'] = row[34];                 p['S'] = row[35]
   
   return p

def commit_pitcher(g_score, row):
   stmt = """
      UPDATE 
         PitcherStats
       SET
         GAME_SCORE_1AGO = %s,
         GAME_SCORE_2AGO = %s,
         GAME_SCORE_3AGO = %s
      WHERE
         ID = %s
      """

   update = (
      g_score[0],
      g_score[1],
      g_score[2],
      row
   )

   commit_to_db(stmt, [update])

def update_pitcher_tbl():
   pitchers = get_pitchers()
   cur_pitcher = create_pitcher_obj(pitchers[0])["NAME"]
   window = []

   for row in range(0,len(pitchers)):
      pitcher = create_pitcher_obj(pitchers[row])
      
      if pitcher["NAME"] != cur_pitcher:
         cur_pitcher = pitcher["NAME"]
         window = []

      # Add new element   
      game_score = pitcher['GAME_SCORE']

      full_window = window + ([None] * (3 - len(window)))

      commit_pitcher(full_window, pitcher["ID"])

      window.insert(0, game_score)
      
      if len(window) > 3:
         window.pop(3)

      print("Count: " + str(row) + " Pitcher: " + cur_pitcher)


if __name__ == '__main__':
   update_pitcher_tbl()
