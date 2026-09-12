-- 1. Teams Table
CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name VARCHAR(100) NOT NULL UNIQUE,
    short_name VARCHAR(10) NOT NULL,
    country VARCHAR(100) NOT NULL
);

-- 2. Venues Table
CREATE TABLE IF NOT EXISTS venues (
    venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    venue_name VARCHAR(150) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    capacity INTEGER DEFAULT 0
);

-- 3. Series Table
CREATE TABLE IF NOT EXISTS series (
    series_id INTEGER PRIMARY KEY AUTOINCREMENT,
    series_name VARCHAR(150) NOT NULL,
    host_country VARCHAR(100) NOT NULL,
    match_type VARCHAR(20) NOT NULL,
    start_date DATE NOT NULL,
    total_matches INTEGER DEFAULT 1
);

-- 4. Players Table
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name VARCHAR(100) NOT NULL,
    team_id INTEGER,
    playing_role VARCHAR(50) NOT NULL,
    batting_style VARCHAR(50),
    bowling_style VARCHAR(50),
    FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE SET NULL
);

-- 5. Matches Table
CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    series_id INTEGER,
    venue_id INTEGER,
    team1_id INTEGER,
    team2_id INTEGER,
    match_description VARCHAR(200),
    match_format VARCHAR(20) NOT NULL,
    match_date DATE NOT NULL,
    toss_winner_id INTEGER,
    toss_decision VARCHAR(10),
    winner_id INTEGER,
    victory_margin INTEGER,
    victory_type VARCHAR(20),
    is_close_match BOOLEAN DEFAULT 0,
    FOREIGN KEY (series_id) REFERENCES series(series_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
    FOREIGN KEY (team1_id) REFERENCES teams(team_id),
    FOREIGN KEY (team2_id) REFERENCES teams(team_id),
    FOREIGN KEY (winner_id) REFERENCES teams(team_id)
);

-- 6. Batting Scorecards Table
CREATE TABLE IF NOT EXISTS batting_scorecards (
    scorecard_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    innings INTEGER NOT NULL,
    batting_position INTEGER NOT NULL,
    runs_scored INTEGER DEFAULT 0,
    balls_faced INTEGER DEFAULT 0,
    fours INTEGER DEFAULT 0,
    sixes INTEGER DEFAULT 0,
    strike_rate REAL DEFAULT 0.0,
    is_out BOOLEAN DEFAULT 1,
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE
);

-- 7. Bowling Scorecards Table
CREATE TABLE IF NOT EXISTS bowling_scorecards (
    bowling_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    innings INTEGER NOT NULL,
    overs_bowled REAL DEFAULT 0.0,
    maiden_overs INTEGER DEFAULT 0,
    runs_conceded INTEGER DEFAULT 0,
    wickets_taken INTEGER DEFAULT 0,
    economy_rate REAL DEFAULT 0.0,
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE
);

-- 8. Fielding & Career Stats Summary
CREATE TABLE IF NOT EXISTS fielding_stats (
    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    catches INTEGER DEFAULT 0,
    stumpings INTEGER DEFAULT 0,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_matches_date ON matches(match_date);
CREATE INDEX IF NOT EXISTS idx_batting_player ON batting_scorecards(player_id);
CREATE INDEX IF NOT EXISTS idx_bowling_player ON bowling_scorecards(player_id);