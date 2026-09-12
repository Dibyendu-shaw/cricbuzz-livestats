import streamlit as st
import sys
import os

# Add parent directory to path so utils can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.api_client import fetch_live_matches

st.set_page_config(page_title="Live Matches", page_icon="⚡", layout="wide")

st.title("⚡ Cricbuzz Live Match Center")
st.caption("Real-time live scores and updates fetched via Cricbuzz REST API")

col1, col2 = st.columns([4, 1])
with col2:
    refresh = st.button("🔄 Refresh Scores")

matches = fetch_live_matches()

if not matches:
    st.info("No live matches currently ongoing.")
else:
    for m in matches:
        with st.container():
            st.markdown(f"### 🏆 {m['series']}")
            st.caption(f"📍 {m['venue']}")
            
            c1, c2, c3 = st.columns([3, 3, 4])
            with c1:
                st.metric(label=f"🏏 {m['team1']}", value=m['team1_score'])
            with c2:
                st.metric(label=f"🏏 {m['team2']}", value=m['team2_score'])
            with c3:
                st.info(f"**Status:** {m['status']}")
            
            st.divider()