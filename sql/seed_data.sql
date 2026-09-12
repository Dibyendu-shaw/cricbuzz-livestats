-- Insert Teams
INSERT OR IGNORE INTO teams (team_id, team_name, short_name, country) VALUES
(1, 'India', 'IND', 'India'),
(2, 'Australia', 'AUS', 'Australia'),
(3, 'England', 'ENG', 'England'),
(4, 'South Africa', 'SA', 'South Africa');

-- Insert Venues (Including capacities > 50000 for Question 4)
INSERT OR IGNORE INTO venues (venue_id, venue_name, city, country, capacity) VALUES
(1, 'Narendra Modi Stadium', 'Ahmedabad', 'India', 132000),
(2, 'Melbourne Cricket Ground', 'Melbourne', 'Australia', 100024),
(3, 'Eden Gardens', 'Kolkata', 'India', 68000),
(4, 'Lord''s Cricket Ground', 'London', 'England', 31100),
(5, 'Wankhede Stadium', 'Mumbai', 'India', 33108);

-- Insert Series (Including series starting in 2024 for Question 8)
INSERT OR IGNORE INTO series (series_id, series_name, host_country, match_type, start_date, total_matches) VALUES
(1, 'Border-Gavaskar Trophy 2024', 'Australia', 'Test', '2024-11-22', 5),
(2, 'India Tour of England 2024', 'England', 'T20I', '2024-07-10', 3),
(3, 'ICC World Cup 2023', 'India', 'ODI', '2023-10-05', 48);

-- Insert Players (India, Australia, England, South Africa)
INSERT OR IGNORE INTO players (player_id, player_name, team_id, playing_role, batting_style, bowling_style) VALUES
(1, 'Virat Kohli', 1, 'Batsman', 'Right-hand bat', 'Right-arm medium'),
(2, 'Rohit Sharma', 1, 'Batsman', 'Right-hand bat', 'Right-arm offbreak'),
(3, 'Hardik Pandya', 1, 'All-rounder', 'Right-hand bat', 'Right-arm fast-medium'),
(4, 'Jasprit Bumrah', 1, 'Bowler', 'Right-hand bat', 'Right-arm fast'),
(5, 'KL Rahul', 1, 'Wicket-keeper', 'Right-hand bat', 'None'),
(6, 'Pat Cummins', 2, 'All-rounder', 'Right-hand bat', 'Right-arm fast'),
(7, 'Steve Smith', 2, 'Batsman', 'Right-hand bat', 'Right-arm legbreak'),
(8, 'Glenn Maxwell', 2, 'All-rounder', 'Right-hand bat', 'Right-arm offbreak'),
(9, 'Mitchell Starc', 2, 'Bowler', 'Left-hand bat', 'Left-arm fast'),
(10, 'Ben Stokes', 3, 'All-rounder', 'Left-hand bat', 'Right-arm fast-medium'),
(11, 'Joe Root', 3, 'Batsman', 'Right-hand bat', 'Right-arm offbreak');

-- Insert Matches (Covering various dates, venues, formats, and close margins)
INSERT OR IGNORE INTO matches (match_id, series_id, venue_id, team1_id, team2_id, match_description, match_format, match_date, toss_winner_id, toss_decision, winner_id, victory_margin, victory_type, is_close_match) VALUES
(1, 3, 1, 1, 2, 'IND vs AUS - World Cup Final', 'ODI', '2023-11-19', 2, 'bowl', 2, 6, 'wickets', 0),
(2, 3, 3, 1, 4, 'IND vs SA - League Match', 'ODI', '2023-11-05', 1, 'bat', 1, 243, 'runs', 0),
(3, 1, 2, 2, 1, 'AUS vs IND - 1st Test', 'Test', '2024-11-22', 1, 'bat', 1, 30, 'runs', 1),
(4, 2, 4, 3, 1, 'ENG vs IND - 1st T20I', 'T20I', '2024-07-10', 3, 'bowl', 1, 4, 'wickets', 1),
(5, 3, 5, 1, 2, 'IND vs AUS - Close ODI Match', 'ODI', '2024-08-15', 1, 'bat', 2, 15, 'runs', 1);

-- Insert Batting Scorecards
INSERT OR IGNORE INTO batting_scorecards (scorecard_id, match_id, player_id, innings, batting_position, runs_scored, balls_faced, fours, sixes, strike_rate, is_out) VALUES
(1, 1, 1, 1, 3, 54, 63, 4, 0, 85.71, 1),
(2, 1, 2, 1, 1, 47, 31, 4, 3, 151.61, 1),
(3, 1, 5, 1, 4, 66, 107, 1, 0, 61.68, 1),
(4, 1, 7, 2, 3, 4, 9, 1, 0, 44.44, 1),
(5, 2, 1, 1, 3, 101, 121, 10, 0, 83.47, 0),
(6, 2, 2, 1, 1, 40, 24, 6, 2, 166.67, 1),
(7, 3, 1, 1, 4, 115, 180, 12, 1, 63.88, 1),
(8, 3, 3, 1, 5, 75, 95, 6, 2, 78.94, 1),
(9, 4, 3, 2, 5, 45, 22, 3, 4, 204.54, 0),
(10, 5, 1, 1, 3, 85, 90, 8, 1, 94.44, 1),
(11, 5, 3, 1, 4, 60, 40, 4, 3, 150.00, 1);

-- Insert Bowling Scorecards
INSERT OR IGNORE INTO bowling_scorecards (bowling_id, match_id, player_id, innings, overs_bowled, maiden_overs, runs_conceded, wickets_taken, economy_rate) VALUES
(1, 1, 4, 2, 9.0, 2, 43, 2, 4.77),
(2, 1, 6, 1, 10.0, 0, 34, 2, 3.40),
(3, 1, 9, 1, 10.0, 0, 55, 3, 5.50),
(4, 2, 4, 2, 5.0, 1, 14, 1, 2.80),
(5, 3, 4, 2, 18.0, 4, 50, 5, 2.77),
(6, 3, 6, 1, 20.0, 3, 65, 4, 3.25),
(7, 4, 4, 1, 4.0, 0, 22, 2, 5.50),
(8, 4, 3, 1, 3.0, 0, 28, 1, 9.33);

-- Insert Fielding Stats
INSERT OR IGNORE INTO fielding_stats (stat_id, player_id, catches, stumpings) VALUES
(1, 1, 150, 0),
(2, 2, 110, 0),
(3, 3, 45, 0),
(4, 5, 80, 15),
(5, 7, 130, 0),
(6, 10, 95, 0);