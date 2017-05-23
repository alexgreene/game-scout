from datetime import date, timedelta
from gamescout_db import db, cur 
from sklearn import linear_model
import pandas as pd
import requests
import json
import re

def createModel():
   #compiled = pd.read_sql('SELECT * FROM Compiled;', con=db)
   data = pd.read_sql('SELECT * FROM Compiled;', con=db)

   cur.execute("""
      SELECT
         COUNT(DISTINCT starting_P_ID)
      FROM
         Compiled
   """)
   num_pitchers = cur.fetchall()[0][0]

   cur.execute("""
      SELECT
         COUNT(DISTINCT P_ID)
      FROM
         Compiled
   """)
   num_batters = cur.fetchall()[0][0]

   #data = compiled.copy()
   data = data[pd.notnull(data['GS1AGO'])]
   data = data[pd.notnull(data['GS2AGO'])]
   data = data[pd.notnull(data['GS3AGO'])]

   labels = data['GOT_HIT']
   data = data[['1_AGO', '2_AGO', '3_AGO', '4_AGO', '5_AGO', '6_AGO', '7_AGO',
                'GS1AGO', 'GS2AGO', 'GS3AGO', 'starting_P_ID', 'P_ID', 
                'hist_AB', 'hist_H']]

   pitch_dummies = pd.get_dummies(data['starting_P_ID']).iloc[:,1:num_pitchers] 
   bat_dummies = pd.get_dummies(data['P_ID']).iloc[:,1:num_batters]

   #data['Gamma'] = data['hist_H'] - (.1 * data['hist_AB'])
   data['Gamma'] = computeGamma(data['hist_H'], data['hist_AB'])

   data = pd.concat([data, pitch_dummies], axis=1)
   data = pd.concat([data, bat_dummies], axis=1)

   data = data.drop('starting_P_ID', 1)
   data = data.drop('P_ID', 1)
   data = data.drop('hist_AB', 1)
   data = data.drop('hist_H', 1)

   y = labels
   x = data

   #train_x = x[:250000]
   #test_x = x[250001:]

   #train_y = y[:250000]
   #test_y = y[250001:]

   model = linear_model.LogisticRegression(class_weight='balanced')
   #model.fit(train_x, train_y)
   model.fit(x, y)

   return (model, pitch_dummies.columns, bat_dummies.columns)

def computeGamma(hits, atbats):
   return hits - (.1 * atbats)

def recentBatterGame(batter_id):
   cur.execute("""
      SELECT
         GOT_HIT, 1_AGO, 2_AGO, 3_AGO, 4_AGO, 
         5_AGO, 6_AGO, 7_AGO, hist_H, hist_AB
      FROM
         Compiled
      WHERE
         P_ID = %s
      ORDER BY G_DATE DESC
      LIMIT 1
   """, [batter_id])

   return cur.fetchall()[0]

def recentPitcherGame(pitcher_id):
   cur.execute("""
      SELECT
         GAME_SCORE_1AGO, GAME_SCORE_2AGO, GAME_SCORE_3AGO
      FROM
         PitcherStats
      WHERE
         P_ID = %s
      ORDER BY G_DATE DESC
      LIMIT 1
   """, [pitcher_id])

   return cur.fetchall()[0]
   
def predictHits(model, pitch_dummies, bat_dummies):
   matchups = []

   cur_season = date.today().year
   tomorrow = date.today() + timedelta(days=1)
   url = "http://gd.mlb.com/components/game/mlb/year_{y}/month_{m:02d}/\
day_{d:02d}/".format(y=tomorrow.year, m=tomorrow.month, d=tomorrow.day)

   games_index = requests.get(url).text
   games = re.findall(r'> (gid.*mlb.*mlb.*)/</a>', games_index)

   p_dummies = dict.fromkeys(pitch_dummies, [0])
   b_dummies = dict.fromkeys(bat_dummies, [0])

   for game_id in games:
      info_url = '{url}{gid}/linescore.json'.format(url=url, gid=game_id)
      response = requests.get(info_url)
      info = json.loads(response.text)
      
      game = info['data']['game']
      matchups.append({
         'pitcher':  game['home_probable_pitcher']['id'],
         'opp_team': game['away_team_name']
         })

      matchups.append({
         'pitcher':  game['away_probable_pitcher']['id'],
         'opp_team': game['home_team_name']
         })

   for matchup in matchups:
      cur.execute("""
         SELECT
            DISTINCT P_ID, NAME 
         FROM 
            BatterStats 
         WHERE 
            TEAM=%s AND YEAR(G_DATE)=%s
      """, [matchup['opp_team'], cur_season]
      )
      rows = cur.fetchall()

      for row in rows:
         batter_id = row[0]
         batter_name = row[1]
         pitcher_id = matchup['pitcher']

         if pitcher_id in p_dummies:
            p_dummies[pitcher_id] = [1]
         p_dummies_df = pd.DataFrame(p_dummies)

         if batter_id in b_dummies:
            b_dummies[batter_id] = [1]
         b_dummies_df = pd.DataFrame(b_dummies)

         batter = recentBatterGame(batter_id)
         pitcher = recentPitcherGame(pitcher_id)

         stats = pd.DataFrame({
            '1_AGO': batter[0],
            '2_AGO': batter[1],
            '3_AGO': batter[2],
            '4_AGO': batter[3],
            '5_AGO': batter[4],
            '6_AGO': batter[5],
            '7_AGO': batter[6],
            'GS1AGO': pitcher[0],
            'GS2AGO': pitcher[1],
            'GS3AGO': pitcher[2],
            'Gamma': [computeGamma(batter[8], batter[9])]
         })
         
         model_input = pd.concat([stats, p_dummies_df, b_dummies_df], axis=1)

         pred = model.predict_proba(model_input)[:,1] 
         print("{0} - {1} ({2}), P: {3}".format(pred, batter_name, batter_id, pitcher_id))


if __name__ == '__main__':
   print("Creating Model...")
   model, pitch_dummies, bat_dummies = createModel()
   print("Generating Predictions...")
   predictHits(model, pitch_dummies, bat_dummies)
