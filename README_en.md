# 🎮 Steam Genre Dashboard

**An interactive Streamlit dashboard for analyzing user trends of Steam games by genre.**

This project visualizes estimated player counts from the top 1,000 Steam games between 2017 and 2020.  
The dashboard provides insights into player activity, market share, language and publisher distribution, and genre-level trends.

---

## Features

- Two main tabs:
  1. **Genre Overview**  
     - Weekly user trends with anomaly detection  
     - Genre-based share of games, users, publishers, and languages  
     - Heatmaps of active user ratios by weekday and hour  
     - Market concentration trends (HHI) and top games  
     - DTW-based genre trend clustering  

  2. **Genre-specific Dashboard**  
     - Select one or more genres  
     - Weekly user stats, HHI trends, and heatmaps  
     - Top 5 games by user share within the selected genre  

---

## Dataset

- Source: [Mendeley Data - Steam Game Dataset](https://data.mendeley.com/datasets/ycy3sy3vj2/1)
- Top 1,000 games with 5-minute interval player counts
- Data period: Dec 2017 – Aug 2020
- Includes metadata (genre, price history, publisher, supported languages)
- Collected from SteamDB and Steamworks API

---

## Run the App

```bash
pip install -r requirements.txt
streamlit run app.py