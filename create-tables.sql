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

create table GamePrediction (
   ID VARCHAR(50) PRIMARY KEY,
   ONE_RUN_GAME BOOLEAN,
   DIFF_WIN_PCT FLOAT
);
