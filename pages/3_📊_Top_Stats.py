import streamlit as st
import pandas as pd
import sys
import os

# Add root directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.api_client import fetch_top_stats

st.set_page_config(page_title="Top Stats", page_icon="📊", layout="wide")

st.title("📊 Tournament Top Stats & Leaderboards")
st.caption("Aggregated tournament leaders fetched via Cricbuzz API")

stats_data = fetch_top_stats()

tab1, tab2 = st.tabs(["🏏 Top Batting Performers (Most Runs)", "🎯 Top Bowling Performers (Most Wickets)"])

with tab1:
    st.subheader("Leading Run Scorers")
    df_batting = pd.DataFrame(stats_data["most_runs"])
    
    # Visual KPI Highlights
    col1, col2, col3 = st.columns(3)
    top_batter = df_batting.iloc[0]
    col1.metric("Tournament Leading Scorer", top_batter["Player"], f"{top_batter['Runs']} Runs")
    col2.metric("Highest Average", f"{df_batting['Average'].max():.2f}", top_batter["Player"])
    col3.metric("Highest Strike Rate", f"{df_batting['Strike_Rate'].max():.2f}", df_batting.loc[df_batting['Strike_Rate'].idxmax()]['Player'])
    
    st.dataframe(df_batting, use_container_width=True, hide_index=True)
    
    # Visual comparison chart
    st.bar_chart(data=df_batting, x="Player", y="Runs", color="#FF4B4B")

with tab2:
    st.subheader("Leading Wicket Takers")
    df_bowling = pd.DataFrame(stats_data["most_wickets"])
    
    # Visual KPI Highlights
    b_col1, b_col2, b_col3 = st.columns(3)
    top_bowler = df_bowling.iloc[0]
    b_col1.metric("Leading Wicket Taker", top_bowler["Player"], f"{top_bowler['Wickets']} Wickets")
    b_col2.metric("Best Average", f"{df_bowling['Average'].min():.2f}", top_bowler["Player"])
    b_col3.metric("Best Economy Rate", f"{df_bowling['Economy'].min():.2f}", df_bowling.loc[df_bowling['Economy'].idxmin()]['Player'])
    
    st.dataframe(df_bowling, use_container_width=True, hide_index=True)
    
    # Visual comparison chart
    st.bar_chart(data=df_bowling, x="Player", y="Wickets", color="#29B5E8")
    