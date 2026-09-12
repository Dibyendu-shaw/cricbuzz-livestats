import streamlit as st
import pandas as pd
import sys
import os

# Link database utility
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.db_connection import get_connection

st.set_page_config(page_title="Player CRUD Manager", page_icon="🛠️", layout="wide")

st.title("🛠️ Player Database Management (CRUD)")
st.caption("Administrative interface to Create, View, Update, and Delete player entries")

# Helper to fetch current players
def fetch_players():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT p.player_id, p.player_name, t.team_name, p.playing_role, p.batting_style, p.bowling_style
        FROM players p
        LEFT JOIN teams t ON p.team_id = t.team_id
        ORDER BY p.player_id DESC
    """, conn)
    conn.close()
    return df

# Helper to fetch team options
def fetch_teams():
    conn = get_connection()
    df = pd.read_sql_query("SELECT team_id, team_name FROM teams", conn)
    conn.close()
    return dict(zip(df["team_name"], df["team_id"]))

teams_dict = fetch_teams()
roles_list = ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"]

# Tab interface for the 4 CRUD operations
tab_view, tab_create, tab_update, tab_delete = st.tabs([
    "📋 View Players (Read)", 
    "➕ Add New Player (Create)", 
    "✏️ Edit Player (Update)", 
    "🗑️ Remove Player (Delete)"
])

# 1. READ
with tab_view:
    st.subheader("Current Registered Players")
    players_df = fetch_players()
    st.dataframe(players_df, use_container_width=True, hide_index=True)
    if st.button("🔄 Refresh Player List"):
        st.rerun()

# 2. CREATE
with tab_create:
    st.subheader("Register New Player")
    with st.form("create_player_form", clear_on_submit=True):
        new_name = st.text_input("Player Name *")
        new_team = st.selectbox("Assign Team", list(teams_dict.keys()))
        new_role = st.selectbox("Playing Role", roles_list)
        new_batting = st.selectbox("Batting Style", ["Right-hand bat", "Left-hand bat"])
        new_bowling = st.text_input("Bowling Style", value="Right-arm medium")
        
        submitted = st.form_submit_button("➕ Add Player")
        if submitted:
            if not new_name.strip():
                st.error("Player name cannot be empty.")
            else:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO players (player_name, team_id, playing_role, batting_style, bowling_style)
                    VALUES (?, ?, ?, ?, ?)
                """, (new_name.strip(), teams_dict[new_team], new_role, new_batting, new_bowling))
                conn.commit()
                conn.close()
                st.success(f"Player '{new_name}' added successfully!")
                st.rerun()

# 3. UPDATE
with tab_update:
    st.subheader("Update Existing Player Details")
    current_players = fetch_players()
    
    if current_players.empty:
        st.info("No players available to update.")
    else:
        player_names = {f"{row['player_id']} - {row['player_name']}": row['player_id'] for _, row in current_players.iterrows()}
        selected_option = st.selectbox("Select Player to Edit", list(player_names.keys()))
        selected_id = player_names[selected_option]
        
        # Load selected player data
        player_row = current_players[current_players["player_id"] == selected_id].iloc[0]
        
        with st.form("update_player_form"):
            up_name = st.text_input("Player Name", value=player_row["player_name"])
            team_index = list(teams_dict.keys()).index(player_row["team_name"]) if player_row["team_name"] in teams_dict else 0
            up_team = st.selectbox("Team", list(teams_dict.keys()), index=team_index)
            role_index = roles_list.index(player_row["playing_role"]) if player_row["playing_role"] in roles_list else 0
            up_role = st.selectbox("Playing Role", roles_list, index=role_index)
            up_batting = st.selectbox("Batting Style", ["Right-hand bat", "Left-hand bat"], index=0 if player_row["batting_style"] == "Right-hand bat" else 1)
            up_bowling = st.text_input("Bowling Style", value=player_row["bowling_style"] or "None")
            
            update_btn = st.form_submit_button("💾 Save Changes")
            if update_btn:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE players
                    SET player_name = ?, team_id = ?, playing_role = ?, batting_style = ?, bowling_style = ?
                    WHERE player_id = ?
                """, (up_name.strip(), teams_dict[up_team], up_role, up_batting, up_bowling, selected_id))
                conn.commit()
                conn.close()
                st.success(f"Details updated for player ID {selected_id}!")
                st.rerun()

# 4. DELETE
with tab_delete:
    st.subheader("Remove Player Record")
    current_players = fetch_players()
    
    if current_players.empty:
        st.info("No players to delete.")
    else:
        delete_names = {f"{row['player_id']} - {row['player_name']}": row['player_id'] for _, row in current_players.iterrows()}
        player_to_delete = st.selectbox("Select Player to Permanently Remove", list(delete_names.keys()))
        target_id = delete_names[player_to_delete]
        
        st.warning(f"⚠️ Warning: This will delete record ID {target_id} permanently.")
        if st.button("🗑️ Confirm Delete"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM players WHERE player_id = ?", (target_id,))
            conn.commit()
            conn.close()
            st.success(f"Player ID {target_id} deleted successfully.")
            st.rerun()
            