import streamlit as st

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 Welcome to Cricbuzz LiveStats")
st.markdown("### Real-Time Cricket Analytics & Relational Query Engine")

st.info("👈 Use the left sidebar to navigate across the platform modules:")

st.markdown("""
1. **🏠 Home**: System architecture and database statistics.
2. **⚡ Live Matches**: Live fixture scores and status tracking.
3. **📊 Top Stats**: Top run scorers and wicket takers.
4. **🔍 SQL Queries**: Analytical SQL query engine with 25 pre-built solutions.
5. **🛠️ CRUD Operations**: Database player management interface.
""")