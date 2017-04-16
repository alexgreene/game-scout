#File: batters.py
#Authors: Alex Greene & Giancarlo Tarantino

from gamescout_db import db, cur
debug_flag = False

def commit_to_db(stmt, data):
   if debug_flag == False:
      cur.executemany(stmt, data)
      db.commit()

def get_batters():
   cur.execute("""
      SELECT
         *
      FROM
         BatterStats
      ORDER BY
         NAME,
         G_DATE ASC
   """)

   row = cur.fetchall()
   return row

def create_batter_obj(row):
   b = {}
   b['ID'] = row[0];                      b['G_DATE'] = row[1]
   b['TEAM'] = row[4];
   b['NAME'] = row[2];                    b['NAME_ABBR'] = row[3]
   b['AT_HOME'] = row[5];                 b['POS'] = row[6]
   b['G_ID'] = row[7];                    b['P_ID'] = row[8]
   b['AB'] = row[9];                      b['AVG'] = row[10]
   b['HITS'] = row[11];                   b['DOUBLES'] = row[12]
   b['TRIPLES'] = row[13];                b['RUNS'] = row[14]
   b['RBI'] = row[15];                    b['HR'] = row[16]
   b['SLG'] = row[17];                    b['OBP'] = row[18]
   b['OPS'] = row[19];                    b['FIELDING_PCT'] = row[20]
   b['BAT_ORDER'] = row[21];              b['BB'] = row[22]
   b['SB'] = row[23];                     b['CAUGHT'] = row[24]
   b['ERROS'] = row[25];                  b['HBP'] = row[26]
   b['K'] = row[27];                      b['SAC_BUNTS'] = row[28]
   b['SAC_FLIES'] = row[29];              b['LOB'] = row[30]
   b['FLY_OUTS'] = row[31];               b['PUTOUTS_FIELDING'] = row[32]
   b['ASSISTS_FIELDING'] = row[33];       b['GROUND_OUTS'] = row[34]
   b['SEA_HITS'] = row[35];               b['SEA_RUNS'] = row[36]
   b['SEA_HR'] = row[37];                 b['SEA_RBI'] = row[38]
   b['SEA_K'] = row[39];                  b['SEA_BB'] = row[40]
   b['1_AGO_AVG'] = row[41];              b['2_AGO_AVG'] = row[42]
   b['3_AGO_AVG'] = row[43];              b['4_AGO_AVG'] = row[44]
   b['5_AGO_AVG'] = row[45];
   
   return b

def commit_batter(avgs, row):
   stmt = """
      UPDATE 
         BatterStats
       SET
         1_AGO_AVG = %s,
         2_AGO_AVG = %s,
         3_AGO_AVG = %s,
         4_AGO_AVG = %s,
         5_AGO_AVG = %s,
         6_AGO_AVG = %s,
         7_AGO_AVG = %s,
         8_AGO_AVG = %s,
         9_AGO_AVG = %s,
         10_AGO_AVG = %s,
         11_AGO_AVG = %s,
         12_AGO_AVG = %s,
         13_AGO_AVG = %s,
         14_AGO_AVG = %s,
         15_AGO_AVG = %s
      WHERE
         ID = %s
      """

   update = (
      avgs[0],
      avgs[1],
      avgs[2],
      avgs[3],
      avgs[4],
      avgs[5],
      avgs[6],
      avgs[7],
      avgs[8],
      avgs[9],
      avgs[10],
      avgs[11],
      avgs[12],
      avgs[13],
      avgs[14],         
      row
   )

   commit_to_db(stmt, [update])

def update_batter_tbl():
   batters = get_batters()
   cur_batter = create_batter_obj(batters[0])["NAME"]
   window = []

   for row in range(0,len(batters)):
      batter = create_batter_obj(batters[row])
      
      if batter["NAME"] != cur_batter:
         cur_batter = batter["NAME"]
         window = []

      # Add new element   
      bat_avg = (float(batter['HITS']) / float(batter['AB'])) if batter['AB'] != 0 else None

      full_window = window + ([None] * (15 - len(window)))

      commit_batter(full_window, batter["ID"])

      window.insert(0, bat_avg)
      
      if len(window) > 15:
         window.pop(15)

      print("Count: " + str(row) + " Batter: " + cur_batter)


if __name__ == '__main__':
   update_batter_tbl()
