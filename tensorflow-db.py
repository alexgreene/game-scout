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
   return True if abs(home - away) == 1 else False


#Builds a game object from a single row
def create_game_obj(row):
   g = {}
   g['G_DATE'] = row[0];            g['G_TYPE'] = row[1]
   g['ID'] = row[2];                g['LEAGUE'] = row[3]
   g['STATUS'] = row[4];            g['START_TIME'] = row[5]
   g['HT'] = row[6];                g['HT_RUNS'] = row[7]
   g['HT_HITS'] = row[8];           g['HT_ERRORS'] = row[9]
   g['AT'] = row[10];               g['AT_RUNS'] = row[11]
   g['AT_HITS'] = row[12];          g['AT_ERRORS'] = row[13]
   g['W_PITCHER'] = row[14];        g['W_PITCHER_WINS'] = row[15]
   g['W_PITCHER_LOSSES'] = row[16]; g['L_PITCHER'] = row[17]
   g['L_PITCHER_WINS'] = row[18];   g['L_PITCHER_LOSSES'] = row[19]
   g['SV_PITCHER'] = row[20];       g['SV_PITCHER_SAVES'] = row[21]
   return g

def create_pitcher_obj(row):
   p = {}
   p['ID'] = row[0];            p['G_DATE'] = row[1]
   p['NAME'] = row[2];          p['NAME_ABBR'] = row[3]
   p['TEAM'] = row[4];          p['AT_HOME'] = row[5]
   p['POS'] = row[6];           p['G_ID'] = row[7]
   p['P_ID'] = row[8];          p['HITS'] = row[9]
   p['RUNS'] = row[10];         p['HR'] = row[11]
   p['BB'] = row[12];           p['K'] = row[13]
   p['SEA_HITS'] = row[14];     p['SEA_RUNS'] = row[15]
   p['SEA_K'] = row[16];        p['SEA_BB'] = row[17]
   p['SEA_L'] = row[18];        p['SEA_W'] = row[19]
   p['SEA_SV'] = row[20];       p['ER'] = row[21]
   p['HOLD'] = row[22];         p['BLOWN_SV'] = row[23]
   p['OUTS'] = row[24];         p['BATTERS_FACED'] = row[25]
   p['GAME_SCORE'] = row[26];   p['ERA'] = row[27]
   p['PITCHES'] = row[28];      p['WIN'] = row[29]
   p['LOSS'] = row[30];         p['SAVE'] = row[31]
   p['NOTE'] = row[32];         p['SEA_ER'] = row[33]
   p['SEA_IP'] = row[34];       p['S'] = row[35]
   return p

#Gets the win pct of a team up until the given date
def get_win_pct(team, date, run_diff_limit):
   if run_diff_limit:
      cur.execute("""
         SELECT
            *
         FROM
            Games
         Where
            (HT = %s or AT = %s)
            AND G_DATE < %s
            AND YEAR(G_DATE) = %s
            AND (HT_RUNS - AT_RUNS == %s OR AT_RUNS - HT_RUNS == %s) 
      """, [team, team, date, str(date.year), run_diff_limit, run_diff_limit])
   else:
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
   totalGames = 0
   wins = 0

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

def get_rivalry_split(home_team, away_team, date):
   # Now let's calculate the w/l record b/w the two teams
   cur.execute("""
      SELECT
         count(*)
      FROM
         Games
      WHERE
         G_DATE < %s
         AND YEAR(G_DATE) = %s
         AND ((HT=%s AND AT=%s AND HT_RUNS>AT_RUNS)
            OR (AT=%s AND HT=%s AND HT_RUNS<AT_RUNS))
   """, [date, str(date.year), game['HT'], game['AT'], game['AT'], game['HT']])
   wins_for_dominant_team = cur.fetchall()[0]

   cur.execute("""
      SELECT
         count(*)
      FROM
         Games
      WHERE
         G_DATE < %s
         AND YEAR(G_DATE) = %s
         AND ((HT=%s AND AT=%s) OR (AT=%s AND HT=%s))
   """, [date, str(date.year), game['HT'], game['AT'], game['AT'], game['HT']])
   total_games_in_rivalry = cur.fetchall()[0]

   rivalry_split = wins_for_dominant_team / total_games_in_rivalry
   return rivalry_split

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
   rs = 0; ra = 0
   rs_win = 0; ra_win = 0
   rs_loss = 0; ra_loss = 0

   if not games:
      return 0
   else:
      for row in games:
         game = create_game_obj(row)

         if game['HT'] == team:
            rs += game['HT_RUNS']
            ra += game['AT_RUNS']

            if rs > ra:
               rs_win += game['HT_RUNS']
               ra_win += game['AT_RUNS']
            else:
               rs_loss += game['HT_RUNS']
               ra_loss += game['AT_RUNS']
         else:
            rs += game['AT_RUNS']
            ra += game['HT_RUNS']

            if rs > ra:
               rs_win += game['AT_RUNS']
               ra_win += game['HT_RUNS']
            else:
               rs_loss += game['AT_RUNS']
               ra_loss += game['HT_RUNS']
            
      return (rs-ra, rs_win/len(games), ra_win/len(games), 
         rs_loss/len(games), ra_loss/len(games))
   
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
   h_diff, h_rs_w, h_ra_w, h_rs_l, h_ra_l = get_run_diff(game['HT'], game['G_DATE'])
   a_diff, a_rs_w, a_ra_w, a_rs_l, a_ra_l = get_run_diff(game['AT'], game['G_DATE'])
   return (h_diff, h_rs_w, h_ra_w, h_rs_l, h_ra_l, 
      a_diff, a_rs_w, a_ra_w, a_rs_l, a_ra_l)

def get_pitcher_stats(game_id):
   cur.execute("""
      SELECT
         *
      FROM
         PitcherStats
      WHERE
         G_ID = %s
      AND AT_HOME = 1
      LIMIT 1
   """, game_id)

   row = cur.fetchall()
   hp = create_pitcher_obj(row[0])

   cur.execute("""
      SELECT
         count(*)
      FROM
         PitcherStats
      WHERE
         P_ID = %s
   """, hp['P_ID'])
   row = cur.fetchall()
   hp_avg_ip = row[0]

   cur.execute("""
      SELECT
         *
      FROM
         PitcherStats
      WHERE
         G_ID = %s
      AND AT_HOME = 0
      LIMIT 1
   """, game_id)

   row = cur.fetchall()
   ap = create_pitcher_obj(row[0])

   cur.execute("""
      SELECT
         count(*)
      FROM
         PitcherStats
      WHERE
         P_ID = %s
   """, hp['P_ID'])
   row = cur.fetchall()
   ap_avg_ip = row[0]

   return (
      x_per_nine(hp['SEA_RUNS'], hp['SEA_IP']),
      x_per_nine(hp['SEA_BB'], hp['SEA_IP']),
      x_per_nine(hp['SEA_HITS'], hp['SEA_IP']),
      x_per_nine(hp['SEA_K'], hp['SEA_IP']),
      hp['SEA_IP'],
      hp['ERA'],
      x_per_nine(ap['SEA_RUNS'], ap['SEA_IP']),
      x_per_nine(ap['SEA_BB'], ap['SEA_IP']),
      x_per_nine(ap['SEA_HITS'], ap['SEA_IP']),
      x_per_nine(ap['SEA_K'], ap['SEA_IP']),
      ap['SEA_IP'],
      ap['ERA'])

def x_per_nine(x, ip):
   return 0 if ip == 0 else (x * 9) / ip

def get_position_averages(home_team, away_team, date):
   cur.execute("""
      SELECT
         SUM(AB), SUM(H)
      FROM
         BatterStats
      Where
         G_ID=%s
         AND G_DATE < %s
         AND YEAR(G_DATE) = %s
         AND POS LIKE '%1B%'
   """, [game_id, date, str(date.year)])

   row = cur.fetchall()

   #fb = sum of AB / sum of H
   
   # and then repeat this for each of the positions

   return (p, c, fb, sb, tb, ss, lf, cf, rf)

#Main function to fill tensorflow db table
def fill_tensorflow():
   game_ids = get_game_ids()

   for game_id in game_ids:
      one_run_game = is_one_run_game(game_id)

      game = get_game(game_id)
      ht_wpct = get_win_pct(game['HT'], game['G_DATE'])
      ht_wpct_1r = get_win_pct(game['HT'], game['G_DATE'], 1)
      ht_wpct_2r = get_win_pct(game['HT'], game['G_DATE'], 2)
      at_wpct = get_win_pct(game['AT'], game['G_DATE'])
      at_wpct_1r = get_win_pct(game['AT'], game['G_DATE'], 1)
      at_wpct_2r = get_win_pct(game['AT'], game['G_DATE'], 2)

      ht_run_diff, ht_avg_rs_w, ht_avg_ra_w, ht_avg_rs_l, ht_avg_ra_l, 
      at_run_diff, at_avg_rs_w, at_avg_ra_w, at_avg_rs_l, at_avg_ra_l = get_run_differentials(game_id)

      hp_r_per9, hp_bb_per9, hp_h_per9, hp_k_per9, hp_ip, hp_era, hp_avg_ip
      ap_r_per9, ap_bb_per9, ap_h_per9, ap_k_per9, ap_ip, ap_era, ap_avg_ip = get_pitcher_stats(game_id)

      rivalry_split = get_rivalry_split(game['HT'], game['AT'], game['G_DATE'])

      cur.execute("""
         INSERT into GamePrediction (
            ID,
            ONE_RUN_GAME,
            HT_WPCT,
            HT_WPCT_1R,
            HT_WPCT_2R,
            AT_WPCT,
            AT_WPCT_1R,
            AT_WPCT_2R,
            HT_RUN_DIFF,
            HT_AVG_RS_WIN,
            HT_AVG_RA_WIN,
            HT_AVG_RS_LOSS,
            HT_AVG_RA_LOSS,
            AT_RUN_DIFF,
            AT_AVG_RS_WIN,
            AT_AVG_RA_WIN,
            AT_AVG_RS_LOSS,
            AT_AVG_RA_LOSS,
            HP_RUNS_PER_9, 
            HP_BB_PER_9, 
            HP_H_PER_9, 
            HP_K_PER_9, 
            HP_IP, 
            HP_ERA,
            HP_AVG_IP,
            AP_RUNS_PER_9, 
            AP_BB_PER_9, 
            AP_H_PER_9, 
            AP_K_PER_9, 
            AP_IP, 
            AP_ERA,
            AP_AVG_IP,
         ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
      """,
      [
         game_id,
         one_run_game,
         ht_wpct,
         ht_wpct_1r,
         ht_wpct_2r,
         at_wpct,
         at_wpct_1r,
         at_wpct_2r,
         ht_run_diff,
         ht_avg_rs_w,
         ht_avg_ra_w,
         ht_avg_rs_l,
         ht_avg_ra_l,
         at_run_diff,
         at_avg_rs_w,
         at_avg_ra_w,
         at_avg_rs_l,
         at_avg_ra_l,
         hp_r_per9, 
         hp_bb_per9, 
         hp_h_per9, 
         hp_k_per9, 
         hp_ip, 
         hp_era,
         hp_avg_ip,
         ap_r_per9, 
         ap_bb_per9, 
         ap_h_per9, 
         ap_k_per9, 
         ap_ip, 
         ap_era,
         ap_avg_ip
      ])
      commit_to_db()

fill_tensorflow()
