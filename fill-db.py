import mlbgame as mlb
import MySQLdb
import config

import MySQLdb

# Connect to the database and setup the db cursor.
db = MySQLdb.connect(host = "localhost",
                     user = "root",
                     passwd = config.db_pass,
                     db = "mlbdata")
cur = db.cursor()

# for each game
    # add game to GAMES table, with an id as primary key
    # for each game, check if 

def fill_db_with_past_games():
    for year in range(2016, 2017):
        for month in range(4, 5):
            for day in range(1, 2):
                game_date = '{}/{}/{}'.format(month, day, year)
                games = mlb.games(year, month, day)
                games = mlb.combine_games(games)
                for game in games:
                    add game metadata to GameStats table
                    cur.execute("""
                        INSERT into GameStats(
                            G_TYPE, 
                            ID, 
                            LEAGUE,
                            STATUS, 
                            START_TIME, 
                            HT, 
                            HT_RUNS, 
                            HT_HITS, 
                            HT_ERRORS, 
                            AT_TEAM, 
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
                            SV_PITCHER_SAVES,
                        ) values(
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
                            game.sv_pitcher_saves)""")

                    # add the innings to Innings table

                    innings = mlb.box_score(game.game_id)
                    for inning in innnings.innings:
                        cur.execute("""
                            INSERT into Innings(
                                G_ID, 
                                G_DATE, 
                                HT,
                                AT, 
                                INNING, 
                                HT_RUNS, 
                                AT_RUNS, 
                            ) values(
                                game.game_id,
                                game_date,
                                game.home_team,
                                game.away_team,
                                inning.inning,
                                inning.home,
                                inning.away)""")

                    players = mlbgame.player_stats(game.game_id)
                    for batter in players['home_batting']:
                        cur.execute("""
                            INSERT into BatterStats(
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
                                SEA_BB,
                            ) values(
                                batter.name_display_first_last,
                                batter.name,
                                game.home_team,
                                True,
                                batter.pos,
                                game.id,
                                batter.id,
                                batter.ab,
                                batter.avg,
                                batter.h,
                                batter.d,
                                batter.t,
                                batter.r,
                                batter.rbi,
                                batter.hr,
                                batter.slg,
                                batter.obp,
                                batter.ops,
                                batter.fldg,
                                batter.bo,
                                batter.bb,
                                batter.sb,
                                batter.cs,
                                batter.e,
                                batter.hpb,
                                batter.so,
                                batter.sac,
                                batter.sf,
                                batter.lob,
                                batter.ao,
                                batter.po,
                                batter.a,
                                batter.go,
                                batter.s_h,
                                batter.s_r,
                                batter.s_hr,
                                batter.s_rbi,
                                batter.s_so,
                                batter.s_bb)""")

                    for batter in players['away_batting']:
                        cur.execute("""
                            INSERT into BatterStats(
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
                                SEA_BB,
                            ) values(
                                batter.name_display_first_last,
                                batter.name,
                                game.away_team,
                                False,
                                batter.pos,
                                game.id,
                                batter.id,
                                batter.ab,
                                batter.avg,
                                batter.h,
                                batter.d,
                                batter.t,
                                batter.r,
                                batter.rbi,
                                batter.hr,
                                batter.slg,
                                batter.obp,
                                batter.ops,
                                batter.fldg,
                                batter.bo,
                                batter.bb,
                                batter.sb,
                                batter.cs,
                                batter.e,
                                batter.hpb,
                                batter.so,
                                batter.sac,
                                batter.sf,
                                batter.lob,
                                batter.ao,
                                batter.po,
                                batter.a,
                                batter.go,
                                batter.s_h,
                                batter.s_r,
                                batter.s_hr,
                                batter.s_rbi,
                                batter.s_so,
                                batter.s_bb)""")

                    for pitcher in players['home_pitching']:
                        cur.execute("""
                            INSERT into PitcherStats(
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
                                W,
                                L,
                                SV,
                                NOTES,
                                SEA_ER,
                                SEA_IP,
                                S
                            ) values(
                                pitcher.name_display_first_last,
                                pitcher.name,
                                game.home_team,
                                True,
                                pitcher.pos,
                                game.id
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
                                pitcher.win,
                                pitcher.loss,
                                pitcher.save,
                                pitcher.note,
                                pitcher.s_er,
                                pitcher.s_ip,
                                pitcher.s)""")

                    for pitcher in players['away_pitching']:
                        cur.execute("""
                            INSERT into PitcherStats(
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
                                W,
                                L,
                                SV,
                                NOTES,
                                SEA_ER,
                                SEA_IP,
                                S
                            ) values(
                                pitcher.name_display_first_last,
                                pitcher.name,
                                game.away_team,
                                False,
                                pitcher.pos,
                                game.id
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
                                pitcher.win,
                                pitcher.loss,
                                pitcher.save,
                                pitcher.note,
                                pitcher.s_er,
                                pitcher.s_ip,
                                pitcher.s)""")

fill_db_with_past_games()

