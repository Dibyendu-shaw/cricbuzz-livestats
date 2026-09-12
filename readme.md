# 🏏 Cricbuzz LiveStats: Real-Time Cricket Analytics & SQL Engine

An end-to-end sports analytics platform that ingests cricket data, manages a normalized relational database in SQLite, provides full CRUD capabilities, and executes 25 graded analytical SQL queries via an interactive Streamlit UI.

---

## 🚀 Key Features

* **Real-Time Match Center**: Ingests live match scores, series standings, and status updates via Cricbuzz REST API endpoints with robust mock fallback resilience.
* **Top Stats & Leaderboards**: Interactive leaderboards showcasing leading run-scorers and wicket-takers with dynamic KPI cards and bar charts.
* **Relational Database (`SQLite`)**: 8 normalized relational tables (`teams`, `venues`, `series`, `players`, `matches`, `batting_scorecards`, `bowling_scorecards`, `fielding_stats`) with optimized B-Tree indexes.
* **25 Graded Analytical SQL Queries**: Complete solutions spanning Beginner, Intermediate, and Advanced queries (CTEs, Window Functions like `DENSE_RANK` and `LAG`, multi-table joins, and aggregate math).
* **Player Database CRUD**: Web-based administrative interface to Create, Read, Update, and Delete player entries.

---

## 🛠️ Tech Stack

* **Frontend**: Streamlit
* **Database**: SQLite3
* **Data Processing**: Pandas
* **API Ingestion**: Requests, Python-dotenv
* **Language**: Python 3.10+

---

## 📂 Project Structure

```text
cricbuzz/
│
├── app.py                      # Main entry point / router
├── pages/
│   ├── 1_🏠_Home.py            # Architecture & database summary
│   ├── 2_⚡_Live_Matches.py     # Real-time scorecards
│   ├── 3_📊_Top_Stats.py        # Tournament leaderboards
│   ├── 4_🔍_SQL_Queries.py      # 25-question SQL analytics runner
│   └── 5_🛠️_CRUD_Operations.py  # Player management portal
├── utils/
│   ├── db_connection.py        # SQLite connection & seed loader
│   └── api_client.py           # REST API client
├── sql/
│   ├── schema.sql              # DDL schema definitions & indexes
│   └── seed_data.sql           # Initial historical match data
├── cricbuzz.db                 # Initialized SQLite database
├── requirements.txt            # Project dependencies
└── README.md                   # Documentation
