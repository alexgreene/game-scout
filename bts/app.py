from gamescout_db import db, cur 
import requests
from datetime import date, timedelta

matchups = []

tomorrow = date.today() + timedelta(days=1)
url = 'http://gd.mlb.com/components/game/mlb/year_{y}/month_{m:02d}/day_{d:02d}/'.format(y=tomorrow.year, m=tomorrow.month, d=tomorrow.day)
games_index = requests.get(url).text
games = re.findall(r'> (gid.*mlb.*mlb.*)/</a>', games_index)
for game_id in games:
    info = "{url}{gid}/linescore.json".format(url=url, gid=game_id)
    
    matchups.append({
      'pitcher': info['home_probable_pitcher']['id'],
      'opp_team': info['away_team_name'],
      })

    matchups.append({
      'pitcher': info['away_probable_pitcher']['id'],
      'opp_team': info['home_team_name'],
      })


for matchup in matchups:
    cur.execute("""SELECT P_ID, NAME FROM BatterStats WHERE TEAM=%s AND YEAR(G_DATE)=2017""", [matchup['opp_team']])
    rows = cur.fetchall()

    for row in rows:
        batter = (row[0], row[1])
        pitcher = matchup['pitcher']
        pred = '0'
        print("{0} - {1} {2}".format(pred, batter[1], pitcher))

