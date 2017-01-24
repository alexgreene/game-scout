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
                games = mlb.games(year, month, day)
                games = mlb.combine_games(games)
                for game in games:
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
                            SV_PITCHER_SAVES) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """, 
                        [
                            game_date,
                            game.game_type,
                            game.game_id,
                            game.game_league,
                            game.game_status,
                            game.game_start_time,
                            game.home_team,
                            game.home_team_runs,
                            game.home_team_hits,
                            game.home_team_errors,
                            game.away_team,
                            game.away_team_runs,
                            game.away_team_hits,
                            game.away_team_errors,
                            game.w_pitcher,
                            game.w_pitcher_wins,
                            game.w_pitcher_losses,
                            game.l_pitcher,
                            game.l_pitcher_wins,
                            game.l_pitcher_losses,
                            game.sv_pitcher,
                            game.sv_pitcher_saves
                        ])
                    db.commit();

                    # add the innings to Innings table

                    innings = mlb.box_score(game.game_id)
                    for inning in innings.innings:
                        if (inning['home'] != 'x'):
                           ht_runs = inning['home'];
                        else:
                           ht_runs = 0;

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
                            game.game_id,
                            game_date,
                            game.home_team,
                            game.away_team,
                            inning['inning'],
                            ht_runs,
                            inning['away']
                        ])
                        db.commit();

                    players = mlb.player_stats(game.game_id)
                    for batter in players['home_batting']:
                        if hasattr(batter, 'slg'):
                           slg = batter.slg;
                        else:
                           slg = None;
                        if hasattr(batter, 'ops'):
                           ops = batter.ops;
                        else:
                           ops = None;
                        if hasattr(batter, 'go'):
                           go = batter.go;
                        else:
                           go = None;
                        if hasattr(batter, 'bo'):
                           bo = batter.bo;
                        else:
                           bo = None;
                        #print game.game_id;
                        #print batter.name_display_first_last;
                        #print batter.bo;
                        cur.execute("""
                            INSERT into BatterStats(
                                G_DATE,
                                NAME, 
                                NAME_ABBR, 
                                TEAM,
                                AT_HOME,
                                POS, 
                                G_ID, 
                                ID, 
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
                                SEA_BB) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """,
                            [
                                game_date,
                                batter.name_display_first_last,
                                batter.name,
                                game.home_team,
                                True,
                                batter.pos,
                                game.game_id,
                                batter.id,
                                batter.ab,
                                batter.avg,
                                batter.h,
                                batter.d,
                                batter.t,
                                batter.r,
                                batter.rbi,
                                batter.hr,
                                slg,
                                batter.obp,
                                ops,
                                batter.fldg,
                                bo,
                                batter.bb,
                                batter.sb,
                                batter.cs,
                                batter.e,
                                batter.hbp,
                                batter.so,
                                batter.sac,
                                batter.sf,
                                batter.lob,
                                batter.ao,
                                batter.po,
                                batter.a,
                                go,
                                batter.s_h,
                                batter.s_r,
                                batter.s_hr,
                                batter.s_rbi,
                                batter.s_so,
                                batter.s_bb
                            ])
                        db.commit();

                    for batter in players['away_batting']:
                        if hasattr(batter, 'slg'):
                           slg = batter.slg;
                        else:
                           slg = None;
                        if hasattr(batter, 'ops'):
                           ops = batter.ops;
                        else:
                           ops = None;
                        if hasattr(batter, 'go'):
                           go = batter.go;
                        else:
                           go = None;
                        if hasattr(batter, 'bo'):
                           bo = batter.bo;
                        else:
                           bo = None;
                        cur.execute("""
                            INSERT into BatterStats(
                                G_DATE,
                                NAME, 
                                NAME_ABBR, 
                                TEAM,
                                AT_HOME,
                                POS, 
                                G_ID, 
                                ID, 
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
                                SEA_BB) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """,
                            [
                                game_date,
                                batter.name_display_first_last,
                                batter.name,
                                game.away_team,
                                False,
                                batter.pos,
                                game.game_id,
                                batter.id,
                                batter.ab,
                                batter.avg,
                                batter.h,
                                batter.d,
                                batter.t,
                                batter.r,
                                batter.rbi,
                                batter.hr,
                                slg,
                                batter.obp,
                                ops,
                                batter.fldg,
                                bo,
                                batter.bb,
                                batter.sb,
                                batter.cs,
                                batter.e,
                                batter.hbp,
                                batter.so,
                                batter.sac,
                                batter.sf,
                                batter.lob,
                                batter.ao,
                                batter.po,
                                batter.a,
                                go,
                                batter.s_h,
                                batter.s_r,
                                batter.s_hr,
                                batter.s_rbi,
                                batter.s_so,
                                batter.s_bb
                            ])
                        db.commit();

                    for pitcher in players['home_pitching']:
                        if hasattr(pitcher, 'win'):
                           win = pitcher.win;
                        else:
                           win = None;
                        if hasattr(pitcher, 'loss'):
                           loss = pitcher.loss;
                        else:
                           loss = None;
                        if hasattr(pitcher, 'save'):
                           save = pitcher.save;
                        else:
                           save = None;
                        if hasattr(pitcher, 'note'):
                           note = pitcher.note;
                        else:
                           note = None;
                        cur.execute("""
                            INSERT into PitcherStats(
                                G_DATE,
                                NAME, 
                                NAME_ABBR, 
                                TEAM,
                                AT_HOME,
                                POS, 
                                G_ID, 
                                ID, 
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
                                S) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """,
                            [
                                game_date,
                                pitcher.name_display_first_last,
                                pitcher.name,
                                game.home_team,
                                True,
                                pitcher.pos,
                                game.game_id,
                                pitcher.id,
                                pitcher.h,
                                pitcher.r,
                                pitcher.hr,
                                pitcher.bb,
                                pitcher.so,
                                pitcher.s_h,
                                pitcher.s_r,
                                pitcher.s_so,
                                pitcher.s_bb,
                                pitcher.l,
                                pitcher.w,
                                pitcher.sv,
                                pitcher.er,
                                pitcher.hld,
                                pitcher.bs,
                                pitcher.out,
                                pitcher.bf,
                                pitcher.game_score,
                                pitcher.era,
                                pitcher.np,
                                win,
                                loss,
                                save,
                                note,
                                pitcher.s_er,
                                pitcher.s_ip,
                                pitcher.s
                            ])
                    db.commit();

                    for pitcher in players['away_pitching']:
                        if hasattr(pitcher, 'win'):
                           win = pitcher.win;
                        else:
                           win = None;
                        if hasattr(pitcher, 'loss'):
                           loss = pitcher.loss;
                        else:
                           loss = None;
                        if hasattr(pitcher, 'save'):
                           save = pitcher.save;
                        else:
                           save = None;
                        if hasattr(pitcher, 'note'):
                           note = pitcher.note;
                        else:
                           note = None;
                        cur.execute("""
                            INSERT into PitcherStats(
                                G_DATE,
                                NAME, 
                                NAME_ABBR, 
                                TEAM,
                                AT_HOME,
                                POS, 
                                G_ID, 
                                ID, 
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
                                S) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """,
                            [
                                game_date,
                                pitcher.name_display_first_last,
                                pitcher.name,
                                game.away_team,
                                False,
                                pitcher.pos,
                                game.game_id,
                                pitcher.id,
                                pitcher.h,
                                pitcher.r,
                                pitcher.hr,
                                pitcher.bb,
                                pitcher.so,
                                pitcher.s_h,
                                pitcher.s_r,
                                pitcher.s_so,
                                pitcher.s_bb,
                                pitcher.l,
                                pitcher.w,
                                pitcher.sv,
                                pitcher.er,
                                pitcher.hld,
                                pitcher.bs,
                                pitcher.out,
                                pitcher.bf,
                                pitcher.game_score,
                                pitcher.era,
                                pitcher.np,
                                win,
                                loss,
                                save,
                                note,
                                pitcher.s_er,
                                pitcher.s_ip,
                                pitcher.s
                            ])
                        db.commit();

fill_db_with_past_games()
