import pandas as pd
from gamescout_db import db, cur
import numpy as np
import math
import checkpoints as ckp

def computeIndex():
   cur.execute("""
      SELECT
         COUNT(*)
      FROM
         Compiled
   """)
   
   return cur.fetchall()[0][0] + 1

def update_compiled(ckp_year, ckp_month, ckp_day):
   year, month, day = ckp.load_checkpoint("checkpoint3.txt")
   last_date = "{0}-{1}-{2}".format(year, month, day)

   curIndex = computeIndex()

   batter_stats_COLUMNS = ['HITS','1_AGO_AVG', '2_AGO_AVG', '3_AGO_AVG', 
                           '4_AGO_AVG', '5_AGO_AVG', '6_AGO_AVG','7_AGO_AVG', 
                           'P_ID','G_ID', 'BAT_ORDER', 'G_DATE', 'TEAM']

   at_bats_COLUMNS = ['BATTER', 'PITCHER', 'G_ID', 'BATTER_LR',
                      'PITCHER_LR', 'G_DATE', 'EVENT']

   pitcher_stats_COLUMNS = ['P_ID', 'G_ID', 'GAME_SCORE', 'BATTERS_FACED', 
                            'TEAM', 'GAME_SCORE_1AGO', 'GAME_SCORE_2AGO', 
                            'GAME_SCORE_3AGO']

   select_bs = 'SELECT * FROM BatterStats WHERE G_DATE > \'{0}\';'.format(last_date)

   batter_stats = pd.read_sql(select_bs, con=db)[batter_stats_COLUMNS]
   batter_stats['GOT_HIT'] = [1 if x > 0 else 0 for x in batter_stats['HITS']]
   batter_stats['NOT_HIT'] = [1 if x == 0 else 0 for x in batter_stats['HITS']]

   batter_stats['1_AGO'] = [0 if x == 0 else 1 for x in batter_stats['1_AGO_AVG']]
   batter_stats['2_AGO'] = [0 if x == 0 else 1 for x in batter_stats['2_AGO_AVG']]
   batter_stats['3_AGO'] = [0 if x == 0 else 1 for x in batter_stats['3_AGO_AVG']]
   batter_stats['4_AGO'] = [0 if x == 0 else 1 for x in batter_stats['4_AGO_AVG']]
   batter_stats['5_AGO'] = [0 if x == 0 else 1 for x in batter_stats['5_AGO_AVG']]
   batter_stats['6_AGO'] = [0 if x == 0 else 1 for x in batter_stats['6_AGO_AVG']]
   batter_stats['7_AGO'] = [0 if x == 0 else 1 for x in batter_stats['7_AGO_AVG']]

   batter_stats = batter_stats[['GOT_HIT', 'NOT_HIT', '1_AGO', '2_AGO', '3_AGO',
                                '4_AGO', '5_AGO', '6_AGO','7_AGO', 'P_ID', 
                                'G_ID', 'BAT_ORDER', 'G_DATE', 'TEAM']]


   select_ps = 'SELECT * FROM PitcherStats WHERE G_DATE > \'{0}\';'.format(last_date)
   pitcher_stats = pd.read_sql(select_ps, con=db)[pitcher_stats_COLUMNS]
   at_bats = pd.read_sql('select * from AtBats;', con=db)[at_bats_COLUMNS]

   hist_AB_series = []
   hist_H_series = []
   OPP_ID_series = []
   GS1AGO_series = []
   GS2AGO_series = []
   GS3AGO_series = []
   order_series = []

   for i in range(0, len(batter_stats)):
      batter = batter_stats.ix[i]
      starting_pitcher = pitcher_stats[pitcher_stats['G_ID'] == batter['G_ID']]
      starting_pitcher = starting_pitcher[pitcher_stats['TEAM'] != batter['TEAM']]
      starting_pitcher = starting_pitcher.sort(['BATTERS_FACED'], ascending=False).head(1)

      matchups = at_bats[at_bats['BATTER'] == batter['P_ID']]
      matchups = matchups[matchups['PITCHER'] == starting_pitcher['P_ID'].iloc[0]]
      matchups = matchups[matchups['G_DATE'] < batter['G_DATE']]
      matchups_hits = matchups[matchups['EVENT'].isin(['Single', 'Double', 'Triple', 'Home Run'])]

      hist_AB = len(matchups)
      hist_H = len(matchups_hits)

      hist_AB_series.append(hist_AB)
      hist_H_series.append(hist_H)
      OPP_ID_series.append(starting_pitcher['P_ID'].iloc[0])
      
      GS1AGO_series.append(starting_pitcher['GAME_SCORE_1AGO'].iloc[0])
      GS2AGO_series.append(starting_pitcher['GAME_SCORE_2AGO'].iloc[0])
      GS3AGO_series.append(starting_pitcher['GAME_SCORE_3AGO'].iloc[0])
      
      order_series.append(batter['BAT_ORDER'])

      if i % 1000 == 0:
         print(i)
      
   batter_stats['hist_AB'] = pd.Series(hist_AB_series)
   batter_stats['hist_H'] = pd.Series(hist_H_series)
   batter_stats['starting_P_ID'] = pd.Series(OPP_ID_series)
   batter_stats['GS1AGO'] = pd.Series(GS1AGO_series)
   batter_stats['GS2AGO'] = pd.Series(GS2AGO_series)
   batter_stats['GS3AGO'] = pd.Series(GS3AGO_series)
   batter_stats['BAT_ORDER'] = pd.Series(order_series)

   #batter_stats.to_sql('Compiled', con=db, if_exists='append')
   batter_stats.index += curIndex
   batter_stats.to_csv('SAVED.csv')

   ckp.save_checkpoint("checkpoint3.txt", ckp_year, ckp_month, ckp_day)

