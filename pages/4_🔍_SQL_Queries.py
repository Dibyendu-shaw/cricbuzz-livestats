import streamlit as st
import pandas as pd
import sys
import os

# Connect to database utility
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.db_connection import get_connection

st.set_page_config(page_title="SQL Analytics Engine", page_icon="🔍", layout="wide")

st.title("🔍 SQL Analytics & Insights Engine")
st.caption("Execute and explore all 25 analytical SQL queries directly on cricbuzz.db")

QUERIES = {
    # ------------------- BEGINNER QUERIES (Q1 - Q7) -------------------
    "Q01: All Indian Players Profile": {
        "description": "Find all players representing India with role, batting, and bowling styles.",
        "difficulty": "Beginner",
        "sql": """
SELECT 
    p.player_name AS "Player Name",
    p.playing_role AS "Playing Role",
    p.batting_style AS "Batting Style",
    p.bowling_style AS "Bowling Style"
FROM players p
INNER JOIN teams t ON p.team_id = t.team_id
WHERE t.team_name = 'India'
ORDER BY p.player_name ASC;
"""
    },
    "Q02: Matches in the Last 30 Days": {
        "description": "Show matches played in the rolling 30-day window relative to current records.",
        "difficulty": "Beginner",
        "sql": """
SELECT 
    m.match_description AS "Match Description",
    t1.team_name AS "Team 1",
    t2.team_name AS "Team 2",
    v.venue_name || ' (' || v.city || ')' AS "Venue & City",
    m.match_date AS "Match Date"
FROM matches m
INNER JOIN teams t1 ON m.team1_id = t1.team_id
INNER JOIN teams t2 ON m.team2_id = t2.team_id
INNER JOIN venues v ON m.venue_id = v.venue_id
WHERE m.match_date >= date((SELECT MAX(match_date) FROM matches), '-30 days')
ORDER BY m.match_date DESC;
"""
    },
    "Q03: Top 10 ODI Run Scorers": {
        "description": "Top 10 aggregate run-getters in ODI format with average and centuries.",
        "difficulty": "Beginner",
        "sql": """
SELECT 
    p.player_name AS "Player Name",
    SUM(b.runs_scored) AS "Total Runs",
    ROUND(CAST(SUM(b.runs_scored) AS REAL) / NULLIF(SUM(CASE WHEN b.is_out = 1 THEN 1 ELSE 0 END), 0), 2) AS "Batting Average",
    SUM(CASE WHEN b.runs_scored >= 100 THEN 1 ELSE 0 END) AS "Centuries"
FROM players p
INNER JOIN batting_scorecards b ON p.player_id = b.player_id
INNER JOIN matches m ON b.match_id = m.match_id
WHERE m.match_format = 'ODI'
GROUP BY p.player_id, p.player_name
ORDER BY "Total Runs" DESC
LIMIT 10;
"""
    },
    "Q04: Large Venues (> 50,000 Capacity)": {
        "description": "Venues with seating capacity greater than 50,000 spectators.",
        "difficulty": "Beginner",
        "sql": """
SELECT 
    venue_name AS "Venue Name",
    city AS "City",
    country AS "Country",
    capacity AS "Capacity"
FROM venues
WHERE capacity > 50000
ORDER BY capacity DESC;
"""
    },
    "Q05: Thrilling Close Finishes": {
        "description": "Matches won by fewer than 20 runs OR by 2 or fewer wickets.",
        "difficulty": "Beginner",
        "sql": """
SELECT 
    m.match_description AS "Match Description",
    m.match_format AS "Format",
    m.match_date AS "Date",
    t.team_name AS "Winning Team",
    m.victory_margin || ' ' || m.victory_type AS "Margin"
FROM matches m
INNER JOIN teams t ON m.winner_id = t.team_id
WHERE (m.victory_type = 'runs' AND m.victory_margin < 20)
   OR (m.victory_type = 'wickets' AND m.victory_margin <= 2)
ORDER BY m.match_date DESC;
"""
    },
    "Q06: Players by Role Breakdown": {
        "description": "Count of players categorized by their primary playing role across all teams.",
        "difficulty": "Beginner",
        "sql": """
SELECT 
    playing_role AS "Playing Role",
    COUNT(*) AS "Total Players"
FROM players
GROUP BY playing_role
ORDER BY "Total Players" DESC;
"""
    },
    "Q07: Venues by Country": {
        "description": "Aggregate count of international venues listed per host country.",
        "difficulty": "Beginner",
        "sql": """
SELECT 
    country AS "Country",
    COUNT(venue_id) AS "Total Stadiums",
    MAX(capacity) AS "Largest Capacity"
FROM venues
GROUP BY country
ORDER BY "Total Stadiums" DESC;
"""
    },

    # ------------------- INTERMEDIATE QUERIES (Q8 - Q17) -------------------
    "Q08: Series Commencing in 2024": {
        "description": "All cricket series initiated in calendar year 2024.",
        "difficulty": "Intermediate",
        "sql": """
SELECT 
    series_name AS "Series",
    host_country AS "Host",
    match_type AS "Format",
    start_date AS "Start Date",
    total_matches AS "Total Matches"
FROM series
WHERE strftime('%Y', start_date) = '2024'
ORDER BY start_date ASC;
"""
    },
    "Q09: Top 5 Economy Bowlers (Min 10 Overs)": {
        "description": "Most economical bowlers across all formats with at least 10 overs delivered.",
        "difficulty": "Intermediate",
        "sql": """
SELECT 
    p.player_name AS "Bowler",
    ROUND(SUM(b.overs_bowled), 1) AS "Overs Bowled",
    SUM(b.runs_conceded) AS "Runs Conceded",
    SUM(b.wickets_taken) AS "Wickets",
    ROUND(CAST(SUM(b.runs_conceded) AS REAL) / NULLIF(SUM(b.overs_bowled), 0), 2) AS "Career Economy"
FROM players p
INNER JOIN bowling_scorecards b ON p.player_id = b.player_id
GROUP BY p.player_id, p.player_name
HAVING SUM(b.overs_bowled) >= 10.0
ORDER BY "Career Economy" ASC
LIMIT 5;
"""
    },
    "Q10: Centuries Scored in Test Matches": {
        "description": "Individual batting innings where a player scored 100 or more runs in Test matches.",
        "difficulty": "Intermediate",
        "sql": """
SELECT 
    p.player_name AS "Batsman",
    b.runs_scored AS "Runs",
    b.balls_faced AS "Balls",
    b.strike_rate AS "Strike Rate",
    m.match_date AS "Date",
    m.match_description AS "Fixture"
FROM batting_scorecards b
INNER JOIN players p ON b.player_id = p.player_id
INNER JOIN matches m ON b.match_id = m.match_id
WHERE m.match_format = 'Test' AND b.runs_scored >= 100
ORDER BY b.runs_scored DESC;
"""
    },
    "Q11: Team Toss Decision Analysis": {
        "description": "Breakdown of how often teams elect to bat vs bowl upon winning the toss.",
        "difficulty": "Intermediate",
        "sql": """
SELECT 
    t.team_name AS "Team",
    SUM(CASE WHEN m.toss_decision = 'bat' THEN 1 ELSE 0 END) AS "Chose to Bat",
    SUM(CASE WHEN m.toss_decision = 'bowl' THEN 1 ELSE 0 END) AS "Chose to Bowl",
    COUNT(*) AS "Total Tosses Won"
FROM matches m
INNER JOIN teams t ON m.toss_winner_id = t.team_id
GROUP BY t.team_id, t.team_name
ORDER BY "Total Tosses Won" DESC;
"""
    },
    "Q12: Five-Wicket Hauls in an Innings": {
        "description": "Bowlers who claimed 5 or more wickets in a single match innings.",
        "difficulty": "Intermediate",
        "sql": """
SELECT 
    p.player_name AS "Bowler",
    b.wickets_taken AS "Wickets",
    b.runs_conceded AS "Runs Given",
    b.overs_bowled AS "Overs",
    m.match_description AS "Match",
    m.match_date AS "Date"
FROM bowling_scorecards b
INNER JOIN players p ON b.player_id = p.player_id
INNER JOIN matches m ON b.match_id = m.match_id
WHERE b.wickets_taken >= 5
ORDER BY b.wickets_taken DESC, b.runs_conceded ASC;
"""
    },
    "Q13: Head-to-Head Win Rate Comparison": {
        "description": "Head-to-head win totals between India and Australia across all formats.",
        "difficulty": "Intermediate",
        "sql": """
SELECT 
    t.team_name AS "Winner",
    COUNT(*) AS "Total Wins"
FROM matches m
INNER JOIN teams t ON m.winner_id = t.team_id
WHERE (m.team1_id = 1 AND m.team2_id = 2) 
   OR (m.team1_id = 2 AND m.team2_id = 1)
GROUP BY t.team_name;
"""
    },
    "Q14: High Strike Rate Finishers (T20I)": {
        "description": "Batters scoring at strike rates > 150.0 in T20I matches (Min 20 balls faced).",
        "difficulty": "Intermediate",
        "sql": """
SELECT 
    p.player_name AS "Batsman",
    b.runs_scored AS "Runs",
    b.balls_faced AS "Balls",
    b.fours AS "4s",
    b.sixes AS "6s",
    b.strike_rate AS "Strike Rate",
    m.match_description AS "Match"
FROM batting_scorecards b
INNER JOIN players p ON b.player_id = p.player_id
INNER JOIN matches m ON b.match_id = m.match_id
WHERE m.match_format = 'T20I' AND b.balls_faced >= 20 AND b.strike_rate >= 150.0
ORDER BY b.strike_rate DESC;
"""
    },
    "Q15: All-Round Performance in Single Match": {
        "description": "Players scoring 30+ runs AND taking 1+ wickets in the very same match.",
        "difficulty": "Intermediate",
        "sql": """
SELECT 
    p.player_name AS "All-Rounder",
    bat.runs_scored AS "Runs Made",
    bowl.wickets_taken AS "Wickets Taken",
    bowl.overs_bowled AS "Overs",
    m.match_description AS "Match"
FROM batting_scorecards bat
INNER JOIN bowling_scorecards bowl ON bat.match_id = bowl.match_id AND bat.player_id = bowl.player_id
INNER JOIN players p ON bat.player_id = p.player_id
INNER JOIN matches m ON bat.match_id = m.match_id
WHERE bat.runs_scored >= 30 AND bowl.wickets_taken >= 1;
"""
    },
    "Q16: Top Wicketkeepers by Dismissals": {
        "description": "Total fielding dismissals (catches + stumpings) for wicketkeepers and fielders.",
        "difficulty": "Intermediate",
        "sql": """
SELECT 
    p.player_name AS "Player",
    p.playing_role AS "Role",
    f.catches AS "Catches",
    f.stumpings AS "Stumpings",
    (f.catches + f.stumpings) AS "Total Dismissals"
FROM fielding_stats f
INNER JOIN players p ON f.player_id = p.player_id
ORDER BY "Total Dismissals" DESC;
"""
    },
    "Q17: Team Win Percentage by Venue": {
        "description": "Stadium win count and total matches hosted to determine ground advantage.",
        "difficulty": "Intermediate",
        "sql": """
SELECT 
    v.venue_name AS "Venue",
    v.city AS "City",
    COUNT(m.match_id) AS "Matches Hosted",
    COUNT(m.winner_id) AS "Decisive Matches"
FROM venues v
LEFT JOIN matches m ON v.venue_id = m.venue_id
GROUP BY v.venue_id, v.venue_name, v.city
ORDER BY "Matches Hosted" DESC;
"""
    },

    # ------------------- ADVANCED QUERIES (Q18 - Q25) -------------------
    "Q18: Toss Advantage & Match Outcome Correlation": {
        "description": "Quantify win percentage when winning the toss vs losing the toss.",
        "difficulty": "Advanced",
        "sql": """
SELECT 
    ROUND(100.0 * SUM(CASE WHEN toss_winner_id = winner_id THEN 1 ELSE 0 END) / COUNT(*), 2) AS "Toss & Match Win %",
    ROUND(100.0 * SUM(CASE WHEN toss_winner_id != winner_id THEN 1 ELSE 0 END) / COUNT(*), 2) AS "Toss Winner Loss %",
    COUNT(*) AS "Total Matches Evaluated"
FROM matches
WHERE winner_id IS NOT NULL;
"""
    },
    "Q19: Rolling Cumulative Runs per Match": {
        "description": "Window Function: Running total of runs scored by players across chronological matches.",
        "difficulty": "Advanced",
        "sql": """
SELECT 
    p.player_name AS "Batsman",
    m.match_date AS "Date",
    b.runs_scored AS "Runs in Match",
    SUM(b.runs_scored) OVER (
        PARTITION BY p.player_id 
        ORDER BY m.match_date ASC
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS "Cumulative Career Runs"
FROM batting_scorecards b
INNER JOIN players p ON b.player_id = p.player_id
INNER JOIN matches m ON b.match_id = m.match_id
ORDER BY p.player_name, m.match_date ASC;
"""
    },
    "Q20: Match Batting Rank per Innings (DENSE_RANK)": {
        "description": "Window Function: Ranking top scorers per match innings using DENSE_RANK.",
        "difficulty": "Advanced",
        "sql": """
SELECT 
    m.match_description AS "Match",
    b.innings AS "Innings",
    p.player_name AS "Batsman",
    b.runs_scored AS "Runs",
    DENSE_RANK() OVER (
        PARTITION BY b.match_id, b.innings 
        ORDER BY b.runs_scored DESC
    ) AS "Innings Rank"
FROM batting_scorecards b
INNER JOIN players p ON b.player_id = p.player_id
INNER JOIN matches m ON b.match_id = m.match_id;
"""
    },
    "Q21: Boundary Contribution Percentage": {
        "description": "Calculate boundary runs (4s and 6s) as a percentage of total runs scored.",
        "difficulty": "Advanced",
        "sql": """
SELECT 
    p.player_name AS "Batsman",
    SUM(b.runs_scored) AS "Total Runs",
    SUM((b.fours * 4) + (b.sixes * 6)) AS "Boundary Runs",
    ROUND(100.0 * SUM((b.fours * 4) + (b.sixes * 6)) / NULLIF(SUM(b.runs_scored), 0), 2) AS "Boundary Run %"
FROM batting_scorecards b
INNER JOIN players p ON b.player_id = p.player_id
GROUP BY p.player_id, p.player_name
HAVING SUM(b.runs_scored) > 50
ORDER BY "Boundary Run %" DESC;
"""
    },
    "Q22: Consecutive Form Tracking (LAG Function)": {
        "description": "Window Function: Compare player runs against their immediate previous match score.",
        "difficulty": "Advanced",
        "sql": """
SELECT 
    p.player_name AS "Batsman",
    m.match_date AS "Match Date",
    b.runs_scored AS "Current Match Runs",
    LAG(b.runs_scored, 1, 0) OVER (
        PARTITION BY p.player_id 
        ORDER BY m.match_date ASC
    ) AS "Previous Match Runs",
    (b.runs_scored - LAG(b.runs_scored, 1, 0) OVER (
        PARTITION BY p.player_id 
        ORDER BY m.match_date ASC
    )) AS "Run Delta"
FROM batting_scorecards b
INNER JOIN players p ON b.player_id = p.player_id
INNER JOIN matches m ON b.match_id = m.match_id;
"""
    },
    "Q23: Highest Partnership Approximation by Match": {
        "description": "CTE analysis evaluating highest paired batting aggregate contributions in an innings.",
        "difficulty": "Advanced",
        "sql": """
WITH MatchInningsTotals AS (
    SELECT 
        b.match_id,
        b.innings,
        SUM(b.runs_scored) AS total_innings_runs,
        MAX(b.runs_scored) AS top_score
    FROM batting_scorecards b
    GROUP BY b.match_id, b.innings
)
SELECT 
    m.match_description AS "Match",
    mit.innings AS "Innings",
    mit.total_innings_runs AS "Total Runs Scored",
    mit.top_score AS "Individual High Score"
FROM MatchInningsTotals mit
INNER JOIN matches m ON mit.match_id = m.match_id
ORDER BY mit.total_innings_runs DESC;
"""
    },
    "Q24: Home vs Away Performance Disparity": {
        "description": "Compare team win percentage when playing within their home nation vs away venues.",
        "difficulty": "Advanced",
        "sql": """
SELECT 
    t.team_name AS "Team",
    COUNT(m.match_id) AS "Total Matches",
    SUM(CASE WHEN m.winner_id = t.team_id THEN 1 ELSE 0 END) AS "Total Wins",
    SUM(CASE WHEN m.winner_id = t.team_id AND v.country = t.country THEN 1 ELSE 0 END) AS "Home Wins",
    SUM(CASE WHEN m.winner_id = t.team_id AND v.country != t.country THEN 1 ELSE 0 END) AS "Away Wins"
FROM teams t
INNER JOIN matches m ON t.team_id = m.team1_id OR t.team_id = m.team2_id
INNER JOIN venues v ON m.venue_id = v.venue_id
GROUP BY t.team_id, t.team_name;
"""
    },
    "Q25: MVP Composite Rating Index": {
        "description": "Compute multi-attribute Player Index: (Runs * 1.0) + (Wickets * 25.0) + (Catches * 10.0).",
        "difficulty": "Advanced",
        "sql": """
SELECT 
    p.player_name AS "Player",
    p.playing_role AS "Role",
    COALESCE(SUM(bat.runs_scored), 0) AS "Total Runs",
    COALESCE(SUM(bowl.wickets_taken), 0) AS "Total Wickets",
    COALESCE(f.catches, 0) AS "Catches",
    ROUND(
        (COALESCE(SUM(bat.runs_scored), 0) * 1.0) +
        (COALESCE(SUM(bowl.wickets_taken), 0) * 25.0) +
        (COALESCE(f.catches, 0) * 10.0), 
        1
    ) AS "Composite MVP Points"
FROM players p
LEFT JOIN batting_scorecards bat ON p.player_id = bat.player_id
LEFT JOIN bowling_scorecards bowl ON p.player_id = bowl.player_id
LEFT JOIN fielding_stats f ON p.player_id = f.player_id
GROUP BY p.player_id, p.player_name, p.playing_role, f.catches
ORDER BY "Composite MVP Points" DESC;
"""
    }
}

selected_q = st.selectbox("Select SQL Query to Execute (Q1 to Q25):", list(QUERIES.keys()))
q_data = QUERIES[selected_q]

col_a, col_b = st.columns([3, 1])
with col_a:
    st.info(f"**Objective:** {q_data['description']}")
with col_b:
    color = "green" if q_data["difficulty"] == "Beginner" else "orange" if q_data["difficulty"] == "Intermediate" else "red"
    st.markdown(f"**Difficulty:** :{color}[{q_data['difficulty']}]")

with st.expander("👁️ View Raw SQL Syntax", expanded=True):
    st.code(q_data["sql"], language="sql")

if st.button("🚀 Execute Query"):
    conn = get_connection()
    try:
        df = pd.read_sql_query(q_data["sql"], conn)
        st.success(f"Execution successful: {len(df)} row(s) returned.")
        st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"SQL Engine Error: {e}")
    finally:
        conn.close()
        