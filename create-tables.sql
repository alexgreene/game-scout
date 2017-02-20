create table Games (
   G_DATE DATE,
   G_TYPE VARCHAR(10),
   ID VARCHAR(50) PRIMARY KEY,
   LEAGUE VARCHAR(10),
   STATUS VARCHAR(10),
   START_TIME VARCHAR(10),
   HT VARCHAR(30),
   HT_RUNS INTEGER,
   HT_HITS INTEGER,
   HT_ERRORS INTEGER,
   AT VARCHAR(30),
   AT_RUNS INTEGER,
   AT_HITS INTEGER,
   AT_ERRORS INTEGER,
   W_PITCHER VARCHAR(30),
   W_PITCHER_WINS INTEGER,
   W_PITCHER_LOSSES INTEGER,
   L_PITCHER VARCHAR(30),
   L_PITCHER_WINS INTEGER,
   L_PITCHER_LOSSES INTEGER,
   SV_PITCHER VARCHAR(30),
   SV_PITCHER_SAVES INTEGER
);

create table Innings (
   TLB_ID INTEGER AUTO_INCREMENT PRIMARY KEY,
   G_ID VARCHAR(50),
   G_DATE DATE,
   HT VARCHAR(30),
   AT VARCHAR(30),
   INNING INTEGER,
   HT_RUNS INTEGER,
   AT_RUNS INTEGER,
   FOREIGN KEY (G_ID) REFERENCES Games (ID)
);

create table BatterStats (
   ID INTEGER AUTO_INCREMENT PRIMARY KEY,
   G_DATE DATE,
   NAME VARCHAR(30),
   NAME_ABBR VARCHAR(30),
   TEAM VARCHAR(30),
   AT_HOME BOOLEAN,
   POS VARCHAR(30),
   G_ID VARCHAR(50),
   P_ID INTEGER,
   AB INTEGER,
   AVG FLOAT,
   HITS INTEGER,
   DOUBLES INTEGER,
   TRIPLES INTEGER,
   RUNS INTEGER,
   RBI INTEGER,
   HR INTEGER,
   SLG FLOAT,
   OBP FLOAT,
   OPS FLOAT,
   FIELDING_PCT FLOAT,
   BAT_ORDER INTEGER,
   BB INTEGER,
   SB INTEGER,
   CAUGHT INTEGER,
   ERRORS INTEGER,
   HBP INTEGER,
   K INTEGER,
   SAC_BUNTS INTEGER,
   SAC_FLIES INTEGER,
   LOB INTEGER,
   FLY_OUTS INTEGER,
   PUTOUTS_FIELDING INTEGER,
   ASSISTS_FIELDING INTEGER,
   GROUND_OUTS INTEGER,
   SEA_HITS INTEGER,
   SEA_RUNS INTEGER,
   SEA_HR   INTEGER,
   SEA_RBI INTEGER,
   SEA_K INTEGER,
   SEA_BB INTEGER,
   FOREIGN KEY (G_ID) REFERENCES Games (ID)
);

create table PitcherStats (
   ID INTEGER AUTO_INCREMENT PRIMARY KEY,
   G_DATE DATE,
   NAME VARCHAR(30),
   NAME_ABBR VARCHAR(20),
   TEAM VARCHAR(30),
   AT_HOME BOOLEAN,
   POS VARCHAR(30),
   G_ID VARCHAR(50),
   P_ID INTEGER,
   HITS INTEGER,
   RUNS INTEGER,
   HR INTEGER,
   BB INTEGER,
   K INTEGER,
   SEA_HITS INTEGER,
   SEA_RUNS INTEGER,
   SEA_K INTEGER,
   SEA_BB INTEGER,
   SEA_L INTEGER,
   SEA_W INTEGER,
   SEA_SV INTEGER,
   ER INTEGER,
   HOLD INTEGER,
   BLOWN_SV INTEGER,
   OUTS INTEGER,
   BATTERS_FACED INTEGER,
   GAME_SCORE INTEGER,
   ERA FLOAT,
   PITCHES INTEGER,
   WIN VARCHAR(10),
   LOSS VARCHAR(10),
   SAVE VARCHAR(10),
   NOTE TEXT,
   SEA_ER INTEGER,
   SEA_IP INTEGER,
   S INTEGER,
   FOREIGN KEY (G_ID) REFERENCES Games (ID)
);

drop table GamePrediction;

create table GamePrediction (
   ID VARCHAR(50) PRIMARY KEY,
   G_DATE DATE,
   HT VARCHAR(30),
   AT VARCHAR(30),
   ONE_RUN_GAME BOOLEAN,
   RIVALRY_SPLIT FLOAT,
   HT_WPCT FLOAT,
   HT_WPCT_1R FLOAT,
   HT_WPCT_2R FLOAT,
   AT_WPCT FLOAT,
   AT_WPCT_1R FLOAT,
   AT_WPCT_2R FLOAT,
   HT_RUN_DIFF FLOAT,
   HT_AVG_RS_WIN FLOAT,
   HT_AVG_RA_WIN FLOAT,
   HT_AVG_RS_LOSS FLOAT,
   HT_AVG_RA_LOSS FLOAT,
   AT_RUN_DIFF FLOAT,
   AT_AVG_RS_WIN FLOAT,
   AT_AVG_RA_WIN FLOAT,
   AT_AVG_RS_LOSS FLOAT,
   AT_AVG_RA_LOSS FLOAT,
   HP_RUNS_PER_9 FLOAT,
   HP_BB_PER_9 FLOAT,
   HP_H_PER_9 FLOAT,
   HP_K_PER_9 FLOAT,
   HP_IP FLOAT,
   HP_ERA FLOAT,
   HP_AVG_IP FLOAT,
   AP_RUNS_PER_9 FLOAT,
   AP_BB_PER_9 FLOAT,
   AP_H_PER_9 FLOAT,
   AP_K_PER_9 FLOAT,
   AP_IP FLOAT,
   AP_ERA FLOAT,
   AP_AVG_IP FLOAT,
   HT_P_AVG FLOAT,
   HT_C_AVG FLOAT,
   HT_1B_AVG FLOAT,
   HT_2B_AVG FLOAT,
   HT_3B_AVG FLOAT,
   HT_SS_AVG FLOAT,
   HT_LF_AVG FLOAT,
   HT_CF_AVG FLOAT,
   HT_RF_AVG FLOAT,
   AT_P_AVG FLOAT,
   AT_C_AVG FLOAT,
   AT_1B_AVG FLOAT,
   AT_2B_AVG FLOAT,
   AT_3B_AVG FLOAT,
   AT_SS_AVG FLOAT,
   AT_LF_AVG FLOAT,
   AT_CF_AVG FLOAT,
   AT_RF_AVG FLOAT,
   HT_AVG_HRS INTEGER,
   AT_AVG_HRS INTEGER
);

create table PastTenGames (
   ID INTEGER AUTO_INCREMENT PRIMARY KEY,
   G_ID VARCHAR(50),
   PAST_GAME VARCHAR(50),
   IS_HOME BOOLEAN   
);
