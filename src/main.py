import streamlit as st
import datetime
import pandas as pd
from graph.anomaly import plot_anomaly_line_chart
from graph.doughnut import genre_game_count, genre_user_share, language_user_share, developer_user_share, plot_doughnut
from graph.heatmap import weekday_heatmap, hourly_heatmap, weekday_hourly_heatmap
from graph.hhi import plot_hhi_line_chart, plot_stacked_bar_chart
from graph.cluster_trend import plot_cluster_trend_scatter, plot_cluster_trend_feature, plot_cluster_barycenter_with_trendline

st.set_page_config(layout="wide")

@st.cache_data
def get_data(filename):
    return pd.read_parquet(f'./src/data/{filename}.parquet')

st.sidebar.title("기간 선택")
start_month = datetime.date(2018, 1, 1)
end_month = datetime.date(2020, 7, 1)
selected_range = st.sidebar.slider(
    "기간 선택 (시작월 ~ 종료월)",
    min_value=start_month,
    max_value=end_month,
    value=(start_month, end_month),
    format="YYYY-MM"
)
selected_start_month, selected_end_month = selected_range

GENRE_COLORS = {
    "Action": "#1f77b4",               # 파랑
    "Adventure": "#aec7e8",            # 연파랑
    "Casual": "#d62728",               # 빨강
    "Early Access": "#ff9896",         # 연빨강
    "Free to Play": "#2ca02c",         # 초록
    "Indie": "#98df8a",                # 연초록
    "Massively Multiplayer": "#ffbb78",# 연주황
    "RPG": "#ff7f0e",                  # 주황
    "Racing": "#9467bd",               # 보라
    "Simulation": "#c5b0d5",           # 연보라
    "Sports": "#8c564b",               # 진한 갈색
    "Strategy": "#c49c94"              # 연갈색
}

def display_legend():
    st.markdown("### 장르별 색상 범례")
    cols = st.columns(4)
    genres = list(GENRE_COLORS.keys())
    for i, genre in enumerate(genres):
        with cols[i % 4]:
            color = GENRE_COLORS[genre]
            st.markdown(f"<div style='display:flex;align-items:center;'>"
                        f"<div style='width:15px;height:15px;background:{color};margin-right:10px;'></div>"
                        f"{genre}</div>", unsafe_allow_html=True)

TAB1, TAB2 = st.tabs(["전체 장르 오버뷰", "장르별 대시보드"])

with TAB1:
    display_legend()
    weekly_df = get_data('weekly_df')
    monthly_meta = get_data('monthly_meta')
    monthly_hour = get_data('monthly_hour')
    monthly_weekday = get_data('monthly_weekday')
    top5_monthly_genre = get_data('top5_monthly_genre')

    filtered_weekly_df = weekly_df[
        (weekly_df['month'].astype(str) >= str(selected_start_month))
        & (weekly_df['month'].astype(str) <= str(selected_end_month))
    ]
    filtered_monthly_meta = monthly_meta[
        (monthly_meta['month'].astype(str) >= str(selected_start_month))
        & (monthly_meta['month'].astype(str) <= str(selected_end_month))
    ]
    filtered_monthly_hour = monthly_hour[
        (monthly_hour['month'].astype(str) >= str(selected_start_month))
        & (monthly_hour['month'].astype(str) <= str(selected_end_month))
    ]
    filtered_monthly_weekday = monthly_weekday[
        (monthly_weekday['month'].astype(str) >= str(selected_start_month))
        & (monthly_weekday['month'].astype(str) <= str(selected_end_month))
    ]
    filtered_top5_monthly_genre = top5_monthly_genre[
        (top5_monthly_genre['month_block'].astype(str) >= str(selected_start_month))
        & (top5_monthly_genre['month_block'].astype(str) <= str(selected_end_month))
    ]

    col1, col2 = st.columns(2)
    with col1:
        st.header("장르별 주간 전체 유저 수 및 이상치")
        st.plotly_chart(plot_anomaly_line_chart(filtered_weekly_df, GENRE_COLORS=GENRE_COLORS))
    with col2:
        st.header("점유율 그래프")
        grid_cols = st.columns(2)
        with grid_cols[0]:
            st.plotly_chart(plot_doughnut(*genre_game_count(filtered_monthly_meta), "장르별 게임 수", GENRE_COLORS=GENRE_COLORS))
            st.plotly_chart(plot_doughnut(*language_user_share(filtered_monthly_meta), "언어 점유율"))
        with grid_cols[1]:
            st.plotly_chart(plot_doughnut(*genre_user_share(filtered_monthly_meta), "장르별 유저 점유율", GENRE_COLORS=GENRE_COLORS))
            st.plotly_chart(plot_doughnut(*developer_user_share(filtered_monthly_meta), "제작사 점유율"))
    st.markdown("### 장르별 hot time")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(weekday_heatmap(filtered_monthly_weekday))
    with col2:
        st.plotly_chart(hourly_heatmap(filtered_monthly_hour))
    st.header("시장 점유율")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 장르별 시장 독점도")
        st.plotly_chart(plot_hhi_line_chart(filtered_weekly_df, GENRE_COLORS=GENRE_COLORS))
    with col2:
        st.markdown("### 장르별 점유율 TOP 5")
        st.plotly_chart(plot_stacked_bar_chart(filtered_top5_monthly_genre, GENRE_COLORS=GENRE_COLORS))
    st.header("트렌드 클러스터")
    col1, col2 = st.columns(2)
    genres, trend, peak_timing, labels, X = plot_cluster_trend_feature(filtered_monthly_meta)
    with col1:
        st.plotly_chart(plot_cluster_trend_scatter(genres, trend, peak_timing, labels))
    with col2:
        st.plotly_chart(plot_cluster_barycenter_with_trendline(labels, X, n_clusters=3))


with TAB2:
    st.title("장르별 대시보드")
    all_genres = monthly_meta['genres'].unique()
    with st.container(border=True):
        selected_genre = st.multiselect("장르 선택", all_genres, default="Action")
    g_dict = dict()
    for g in selected_genre:
        g_dict[g] = get_data(f'wday_hour_{g}')
    
    st.header("선택 장르 주간 전체 유저 수 및 이상치")
    st.plotly_chart(plot_anomaly_line_chart(filtered_weekly_df, selected_genre=selected_genre))
    
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        st.header("선택 장르 시장독점도")
        st.plotly_chart(plot_hhi_line_chart(filtered_weekly_df, selected_genre=selected_genre))
    with col2:
        st.header("언어 점유율")
        st.plotly_chart(plot_doughnut(*language_user_share(filtered_monthly_meta, selected_genre=selected_genre), "언어 점유율"))
    with col3:
        st.header("제작사 점유율")
        st.plotly_chart(plot_doughnut(*developer_user_share(filtered_monthly_meta, selected_genre=selected_genre), "제작사 점유율"))
    
        
    st.write("장르별 버튼:")

    g = st.radio(
        "장르별 버튼",
        options=selected_genre,
        horizontal=True,
        label_visibility="collapsed"  # 라벨 숨김(공백 최소화)
    ) if selected_genre else None

    col1, col2 = st.columns(2)
    with col1:
        g_weekday_hour = get_data(f'wday_hour_{g}')
        st.header("요일-시간대별 hot time")
        st.plotly_chart(weekday_hourly_heatmap(g_weekday_hour, genre=g))

    with col2:
        st.header(f"{g} 장르 점유율 TOP 5")
        st.plotly_chart(plot_stacked_bar_chart(filtered_top5_monthly_genre, selected_genre=g))
        