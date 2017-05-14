import mlbgame as mlb
import MySQLdb
from config import config
from datetime import date
import checkpoints as ckp

# Connect to the database and setup the db cursor.
db = MySQLdb.connect(host = "localhost",
                     user = "root",
                     passwd = config['password'],
                     db = "mlbdata")
cur = db.cursor()

###### INSTRUCTIONS #######
# False: SQL commands will be committed to your db
# True: SQL commands will not commit, no data enters db.
debug_flag = False

def commit_to_db():
   if debug_flag == False:
      db.commit()

def array_to_dict(arr):
    arr_dict = {}
    for el in arr:
        arr_dict[el] = 0

    return arr_dict

def guarant_type(val, attr):
    num_reqs = array_to_dict(
        ['id', 'ab', 'avg', 'h', 'd', 't', 'r', 'rbi', 
        'hr', 'slg', 'obp', 'ops', 'fldg', 'bo', 'bb', 
        'sb', 'cs', 'e', 'hbp', 'so', 'sac', 'sf', 
        'lob', 'ao', 'po', 'a', 'go', 's_h', 's_r',
        's_hr', 's_rbi', 's_so', 's_bb', 'era', 'l', 'w', 'sv', 'er', 'hld',
        'bs', 'out', 'bf', 'game_score', 'np', 's_er', 's_ip', 's', 
        'home_team_hits', 'home_team_runs', 'home_team_errors', 
        'away_team_hits', 'away_team_runs', 'away_team_errors', 
        'w_pitcher_wins', 'w_pitcher_losses', 'l_pitcher_wins',
        'l_pitcher_losses', 'sv_pitcher_saves'])
    
    if attr not in num_reqs:
        return val
    try:
        float(val)
        return val
    except:
        return 0

def ensure_attr_batter(batter):
    new_batter = {}
    for attr in ['name_display_first_last', 'name', 'pos', 'id', 'ab', 'avg',
    'h', 'd', 't', 'r', 'rbi', 'hr', 'slg', 'obp', 'ops', 'fldg', 'bo', 'bb',
    'sb', 'cs', 'e', 'hbp', 'so', 'sac', 'sf', 'lob', 'ao', 'po', 'a', 'go',
    's_h', 's_r', 's_hr', 's_rbi', 's_so', 's_bb']:

        if hasattr(batter, attr):
            new_batter[attr] = getattr(batter, attr)
        else:
            new_batter[attr] = None

        new_batter[attr] = guarant_type(new_batter[attr], attr)

    return new_batter


def ensure_attr_pitcher(pitcher):
    new_pitcher = {}
    for attr in ['name_display_first_last', 'name', 'pos', 'id', 'h', 'r', 'hr', 
    'bb', 'so', 's_h', 's_r', 's_so', 's_bb', 'l', 'w', 'sv', 'er', 'hld', 'bs', 
    'out', 'bf', 'game_score', 'era', 'np', 'win', 'loss', 'save', 'note', 's_er', 
    's_ip', 's']:

        if hasattr(pitcher, attr):
            new_pitcher[attr] = getattr(pitcher, attr)
        else:
            new_pitcher[attr] = None

        new_pitcher[attr] = guarant_type(new_pitcher[attr], attr)

    return new_pitcher

def ensure_attr_game(game):                            
    new_game = {}
    for attr in ['game_type', 'game_id', 'game_league', 'game_status', 
                 'game_start_time', 'home_team', 'home_team_runs',
                 'home_team_hits', 'home_team_errors', 'away_team', 
                 'away_team_runs', 'away_team_hits', 'away_team_errors',
                 'w_pitcher', 'w_pitcher_wins', 'w_pitcher_losses', 
                 'l_pitcher', 'l_pitcher_wins', 'l_pitcher_losses',
                 'sv_pitcher', 'sv_pitcher_saves']:

        if hasattr(game, attr):
            new_game[attr] = getattr(game, attr)
        else:
            if attr == 'game_id':
                new_game[attr] = '_'
            else:
                new_game[attr] = None

        new_game[attr] = guarant_type(new_game[attr], attr)

    return new_game

def num_days_in(month):
   return {
      3: 31, 4: 30, 5: 31,
      6: 30, 7: 31, 8: 31,
      9: 30, 10: 31
   }[month]

def fill_db_with_past_games():
    ckp_year, ckp_month, ckp_day = ckp.load_checkpoint("checkpoint1.txt")

    for year in range(ckp_year, date.today().year + 1):
        start_month = 3 if year != ckp_year else ckp_month
        end_month = 10 if year != date.today().year else date.today().month
        for month in range(start_month, end_month + 1):
            start_day = 1 if year != ckp_year or month != ckp_month else ckp_day + 1
            end_day = num_days_in(month) if year != date.today().year or  month != date.today().month else date.today().day - 1
            for day in range(start_day, end_day + 1):

                game_date = date(year, month, day).isoformat();
                games = mlb.games(year, month, day)
                games = mlb.combine_games(games)
                for game in games:
                    print(game.game_id)
                    new_game = ensure_attr_game(game)
                    cur.execute("""
                        INSERT into Games(
                            G_DATE,
                            G_TYPE, 
                            ID, 
                            LEAGUE,
                            STATUS, 
                            START_TIME, 
                            HT, 
                            HT_RUNS, 
                            HT_HITS, 
                            HT_ERRORS, 
                            AT, 
                            AT_RUNS, 
                            AT_HITS, 
                            AT_ERRORS, 
                            W_PITCHER, 
                            W_PITCHER_WINS, 
                            W_PITCHER_LOSSES, 
                            L_PITCHER, 
                            L_PITCHER_WINS, 
                            L_PITCHER_LOSSES, 
                            SV_PITCHER, 
                            SV_PITCHER_SAVES) values(%s,%s,%s,%s,%s,%s,%s,
                            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            ON DUPLICATE KEY UPDATE ID=ID
                        """, 
                        [
                            game_date,
                            new_game['game_type'],
                            new_game['game_id'],
                            new_game['game_league'],
                            new_game['game_status'],
                            new_game['game_start_time'],
                            new_game['home_team'],
                            new_game['home_team_runs'],
                            new_game['home_team_hits'],
                            new_game['home_team_errors'],
                            new_game['away_team'],
                            new_game['away_team_runs'],
                            new_game['away_team_hits'],
                            new_game['away_team_errors'],
                            new_game['w_pitcher'],
                            new_game['w_pitcher_wins'],
                            new_game['w_pitcher_losses'],
                            new_game['l_pitcher'],
                            new_game['l_pitcher_wins'],
                            new_game['l_pitcher_losses'],
                            new_game['sv_pitcher'],
                            new_game['sv_pitcher_saves']
                        ])
                    commit_to_db()

                    # add the innings to Innings table
                    try:
                        innings = mlb.box_score(game.game_id)

                        if hasattr(innings, 'innings'):
                            for inning in innings.innings:
                                if (inning['home'] != 'x'):
                                   ht_runs = inning['home']
                                else:
                                   ht_runs = 0

                                cur.execute("""
                                    INSERT into Innings(
                                        G_ID, 
                                        G_DATE, 
                                        HT,
                                        AT, 
                                        INNING, 
                                        HT_RUNS, 
                                        AT_RUNS 
                                    ) values(%s,%s,%s,%s,%s,%s,%s)
                                """,
                                [
                                    new_game['game_id'],
                                    game_date,
                                    new_game['home_team'],
                                    new_game['away_team'],
                                    inning['inning'],
                                    ht_runs,
                                    inning['away']
                                ])
                                commit_to_db()
                    except:
                        print("> box score not found")

                    try:
                        players = mlb.player_stats(new_game['game_id'])
                    except:
                        print("> player stats not found")
                        continue
                    for batter in players['home_batting']:
                        new_batter = ensure_attr_batter(batter)
                        
                        cur.execute("""
                            INSERT into BatterStats(
                                G_DATE,
                                NAME, 
                                NAME_ABBR, 
                                TEAM,
                                AT_HOME,
                                POS, 
                                G_ID, 
                                P_ID, 
                                AB, 
                                AVG, 
                                HITS, 
                                DOUBLES, 
                                TRIPLES, 
                                RUNS, 
                                RBI, 
                                HR, 
                                SLG, 
                                OBP, 
                                OPS, 
                                FIELDING_PCT, 
                                BAT_ORDER, 
                                BB,
                                SB, 
                                CAUGHT,
                                ERRORS,
                                HBP,
                                K,
                                SAC_BUNTS,
                                SAC_FLIES,
                                LOB,
                                FLY_OUTS,
                                PUTOUTS_FIELDING,
                                ASSISTS_FIELDING,
                                GROUND_OUTS,
                                SEA_HITS,
                                SEA_RUNS,
                                SEA_HR,
                                SEA_RBI,
                                SEA_K,
                                SEA_BB) values(%s,%s,%s,%s,%s,%s,%s,%s,
                                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                %s,%s,%s,%s,%s,%s)
                            """,
                            [
                                game_date,
                                new_batter['name_display_first_last'],
                                new_batter['name'],
                                game.home_team,
                                True,
                                new_batter['pos'],
                                new_game['game_id'],
                                new_batter['id'],
                                new_batter['ab'],
                                new_batter['avg'],
                                new_batter['h'],
                                new_batter['d'],
                                new_batter['t'],
                                new_batter['r'],
                                new_batter['rbi'],
                                new_batter['hr'],
                                new_batter['slg'],
                                new_batter['obp'],
                                new_batter['ops'],
                                new_batter['fldg'],
                                new_batter['bo'],
                                new_batter['bb'],
                                new_batter['sb'],
                                new_batter['cs'],
                                new_batter['e'],
                                new_batter['hbp'],
                                new_batter['so'],
                                new_batter['sac'],
                                new_batter['sf'],
                                new_batter['lob'],
                                new_batter['ao'],
                                new_batter['po'],
                                new_batter['a'],
                                new_batter['go'],
                                new_batter['s_h'],
                                new_batter['s_r'],
                                new_batter['s_hr'],
                                new_batter['s_rbi'],
                                new_batter['s_so'],
                                new_batter['s_bb']
                            ])
                        commit_to_db()

                    for batter in players['away_batting']:
                        new_batter = ensure_attr_batter(batter)
                        cur.execute("""
                            INSERT into BatterStats(
                                G_DATE,
                                NAME, 
                                NAME_ABBR, 
                                TEAM,
                                AT_HOME,
                                POS, 
                                G_ID, 
                                P_ID, 
                                AB, 
                                AVG, 
                                HITS, 
                                DOUBLES, 
                                TRIPLES, 
                                RUNS, 
                                RBI, 
                                HR, 
                                SLG, 
                                OBP, 
                                OPS, 
                                FIELDING_PCT, 
                                BAT_ORDER, 
                                BB,
                                SB, 
                                CAUGHT,
                                ERRORS,
                                HBP,
                                K,
                                SAC_BUNTS,
                                SAC_FLIES,
                                LOB,
                                FLY_OUTS,
                                PUTOUTS_FIELDING,
                                ASSISTS_FIELDING,
                                GROUND_OUTS,
                                SEA_HITS,
                                SEA_RUNS,
                                SEA_HR,
                                SEA_RBI,
                                SEA_K,
                                SEA_BB) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                %s,%s,%s)
                            """,
                            [
                                game_date,
                                new_batter['name_display_first_last'],
                                new_batter['name'],
                                game.away_team,
                                False,
                                new_batter['pos'],
                                new_game['game_id'],
                                new_batter['id'],
                                new_batter['ab'],
                                new_batter['avg'],
                                new_batter['h'],
                                new_batter['d'],
                                new_batter['t'],
                                new_batter['r'],
                                new_batter['rbi'],
                                new_batter['hr'],
                                new_batter['slg'],
                                new_batter['obp'],
                                new_batter['ops'],
                                new_batter['fldg'],
                                new_batter['bo'],
                                new_batter['bb'],
                                new_batter['sb'],
                                new_batter['cs'],
                                new_batter['e'],
                                new_batter['hbp'],
                                new_batter['so'],
                                new_batter['sac'],
                                new_batter['sf'],
                                new_batter['lob'],
                                new_batter['ao'],
                                new_batter['po'],
                                new_batter['a'],
                                new_batter['go'],
                                new_batter['s_h'],
                                new_batter['s_r'],
                                new_batter['s_hr'],
                                new_batter['s_rbi'],
                                new_batter['s_so'],
                                new_batter['s_bb']
                            ])
                        commit_to_db()

                    for pitcher in players['home_pitching']:
                        new_pitcher = ensure_attr_pitcher(pitcher)
                        cur.execute("""
                            INSERT into PitcherStats(
                                G_DATE,
                                NAME, 
                                NAME_ABBR, 
                                TEAM,
                                AT_HOME,
                                POS, 
                                G_ID, 
                                P_ID, 
                                HITS, 
                                RUNS, 
                                HR, 
                                BB, 
                                K, 
                                SEA_HITS, 
                                SEA_RUNS, 
                                SEA_K, 
                                SEA_BB, 
                                SEA_L, 
                                SEA_W, 
                                SEA_SV, 
                                ER, 
                                HOLD, 
                                BLOWN_SV,
                                OUTS,
                                BATTERS_FACED,
                                GAME_SCORE,
                                ERA,
                                PITCHES,
                                WIN,
                                LOSS,
                                SAVE,
                                NOTE,
                                SEA_ER,
                                SEA_IP,
                                S) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """,
                            [
                                game_date,
                                new_pitcher['name_display_first_last'],
                                new_pitcher['name'],
                                game.home_team,
                                True,
                                new_pitcher['pos'],
                                new_game['game_id'],
                                new_pitcher['id'],
                                new_pitcher['h'],
                                new_pitcher['r'],
                                new_pitcher['hr'],
                                new_pitcher['bb'],
                                new_pitcher['so'],
                                new_pitcher['s_h'],
                                new_pitcher['s_r'],
                                new_pitcher['s_so'],
                                new_pitcher['s_bb'],
                                new_pitcher['l'],
                                new_pitcher['w'],
                                new_pitcher['sv'],
                                new_pitcher['er'],
                                new_pitcher['hld'],
                                new_pitcher['bs'],
                                new_pitcher['out'],
                                new_pitcher['bf'],
                                new_pitcher['game_score'],
                                new_pitcher['era'],
                                new_pitcher['np'],
                                new_pitcher['win'],
                                new_pitcher['loss'],
                                new_pitcher['save'],
                                new_pitcher['note'],
                                new_pitcher['s_er'],
                                new_pitcher['s_ip'],
                                new_pitcher['s']
                            ])
                    commit_to_db()

                    for pitcher in players['away_pitching']:
                        new_pitcher = ensure_attr_pitcher(pitcher)
                        cur.execute("""
                            INSERT into PitcherStats(
                                G_DATE,
                                NAME, 
                                NAME_ABBR, 
                                TEAM,
                                AT_HOME,
                                POS, 
                                G_ID, 
                                P_ID, 
                                HITS, 
                                RUNS, 
                                HR, 
                                BB, 
                                K, 
                                SEA_HITS, 
                                SEA_RUNS, 
                                SEA_K, 
                                SEA_BB, 
                                SEA_L, 
                                SEA_W, 
                                SEA_SV, 
                                ER, 
                                HOLD, 
                                BLOWN_SV,
                                OUTS,
                                BATTERS_FACED,
                                GAME_SCORE,
                                ERA,
                                PITCHES,
                                WIN,
                                LOSS,
                                SAVE,
                                NOTE,
                                SEA_ER,
                                SEA_IP,
                                S) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """,
                            [
                                game_date,
                                new_pitcher['name_display_first_last'],
                                new_pitcher['name'],
                                game.away_team,
                                False,
                                new_pitcher['pos'],
                                new_game['game_id'],
                                new_pitcher['id'],
                                new_pitcher['h'],
                                new_pitcher['r'],
                                new_pitcher['hr'],
                                new_pitcher['bb'],
                                new_pitcher['so'],
                                new_pitcher['s_h'],
                                new_pitcher['s_r'],
                                new_pitcher['s_so'],
                                new_pitcher['s_bb'],
                                new_pitcher['l'],
                                new_pitcher['w'],
                                new_pitcher['sv'],
                                new_pitcher['er'],
                                new_pitcher['hld'],
                                new_pitcher['bs'],
                                new_pitcher['out'],
                                new_pitcher['bf'],
                                new_pitcher['game_score'],
                                new_pitcher['era'],
                                new_pitcher['np'],
                                new_pitcher['win'],
                                new_pitcher['loss'],
                                new_pitcher['save'],
                                new_pitcher['note'],
                                new_pitcher['s_er'],
                                new_pitcher['s_ip'],
                                new_pitcher['s']
                            ])
                        commit_to_db()
                ckp.save_checkpoint("checkpoint1.txt", year, month, day)

fill_db_with_past_games()
