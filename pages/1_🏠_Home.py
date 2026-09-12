import streamlit as st
import sys
import os

# Link database utility
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.db_connection import get_connection

st.set_page_config(page_title="Cricbuzz LiveStats - System Overview", page_icon="🏠", layout="wide")

st.title("🏏 Cricbuzz LiveStats: System Documentation & Architecture")
st.caption("End-to-End Cricket Analytics Platform powered by Streamlit, SQLite, and Cricbuzz REST API")

# Top Metrics Row (Real-time DB Summary)
conn = get_connection()
cursor = conn.cursor()
try:
    total_teams = cursor.execute("SELECT COUNT(*) FROM teams").fetchone()[0]
    total_players = cursor.execute("SELECT COUNT(*) FROM players").fetchone()[0]
    total_matches = cursor.execute("SELECT COUNT(*) FROM matches").fetchone()[0]
    total_venues = cursor.execute("SELECT COUNT(*) FROM venues").fetchone()[0]
except Exception:
    total_teams, total_players, total_matches, total_venues = 0, 0, 0, 0
finally:
    conn.close()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Registered Teams", total_teams)
c2.metric("Tracked Players", total_players)
c3.metric("Matches Recorded", total_matches)
c4.metric("International Venues", total_venues)

st.divider()

# Architectural Walkthrough
st.subheader("🛠️ Technology Stack & Architecture")
t1, t2, t3 = st.columns(3)

with t1:
    st.markdown("""
    **Frontend Layer**
    * **Streamlit Framework**: Multi-page dynamic interface
    * **Interactive Visualizations**: Metric cards, leaderboards, and data charts
    * **Responsive Layouts**: Wide aspect dataframes and tab navigation
    """)

with t2:
    st.markdown("""
    **Data & Persistence Layer**
    * **SQLite Engine**: Embedded relational storage (`cricbuzz.db`)
    * **Optimized Schema**: 8 normalized relational tables
    * **Performance Indexes**: B-Tree indices on dates and player keys
    """)

with t3:
    st.markdown("""
    **API & Integration Layer**
    * **REST Client**: HTTP ingestion using Python `requests`
    * **Fallback Resilience**: Mock fallback data if network/API limits trigger
    * **Environment Config**: Secure API key management via `.env`
    """)

st.divider()

# Module Guide
st.subheader("🧭 Platform Navigation Guide")
st.markdown("""
* **⚡ Live Matches**: Live scores, series details, and match progression fetched dynamically from the Cricbuzz API.
* **📊 Top Stats**: Batting and bowling leaderboards, run charts, and player performance averages.
* **🔍 SQL Queries**: Interactive analytics console executing 25 queries across beginner, intermediate, and advanced tiers (CTEs, Window Functions, DENSE_RANK, LAG).
* **🛠️ CRUD Operations**: Administrative management portal to Create, Read, Update, and Delete player records in the database.
""")