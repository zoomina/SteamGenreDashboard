import pandas as pd
import numpy as np
import plotly.graph_objects as go

LANGUAGE_USER_SHARE = {
    'English': 0.335,
    'Simplified Chinese': 0.337,
    'Russian': 0.082,
    'Spanish - Spain': 0.046,
    'Portuguese - Brazil': 0.028,
    'German': 0.025,
    'Korean': 0.022,
    'French': 0.021,
    'Japanese': 0.017,
    'Turkish': 0.017,
    'Polish': 0.015,
    'Traditional Chinese': 0.01,
    'Italian': 0.007,
    'Thai': 0.006,
    'Other': 0.032
}

def genre_game_count(df):
    genre_count = df['genres'].value_counts()
    return genre_count.index.tolist(), genre_count.values.tolist(), False

def genre_user_share(df):
    genre_user = df.groupby('genres')['monthly_user'].sum()
    share = genre_user / genre_user.sum()
    return share.index, share.values, False

def language_user_share(df, selected_genre=None):
    # 선택된 장르 없을 시 전체 장르 데이터 사용
    if selected_genre is None:
        df_g = df
    else:
        df_g = df[df['genres'].isin(selected_genre)]

    language_user = {}
    for _, row in df_g.iterrows():
        langs = row['languages']
        user = row['monthly_user']
        # langs가 None이거나 비어있으면 건너뜀
        if langs is None or len(langs) == 0 or user is None or pd.isna(user) or user == 0:
            continue
        total_weight = sum(LANGUAGE_USER_SHARE.get(l, LANGUAGE_USER_SHARE['Other']) for l in langs)
        if total_weight == 0:
            continue
        for l in langs:
            if l in LANGUAGE_USER_SHARE:
                weight = LANGUAGE_USER_SHARE[l]
                language_user[l] = language_user.get(l, 0) + user * (weight / total_weight)
            else:
                weight = LANGUAGE_USER_SHARE['Other']
                language_user['Other'] = language_user.get('Other', 0) + user * (weight / total_weight)
    total = sum(language_user.values())
    if total == 0:
        return [], []
    share = {k: v / total for k, v in language_user.items()}
    return list(share.keys()), list(share.values()), True

def developer_user_share(df, selected_genre=None):
    # 선택된 장르 없을 시 전체 장르 데이터 사용
    if selected_genre is None:
        df_g = df
    else:
        df_g = df[df['genres'].isin(selected_genre)]

    df_dev = df_g.explode('developers').copy()
    dev_user = df_dev.groupby('developers')['monthly_user'].sum()
    share = dev_user / dev_user.sum()
    return share.index, share.values, True

def plot_doughnut(labels, values, show_legend, title, GENRE_COLORS=None):
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        hoverinfo='label+percent+value',
        textinfo='percent',
        textposition='inside',
        marker=dict(colors=list(GENRE_COLORS.values())) if GENRE_COLORS else None
    )])
    fig.update_layout(
        title_text=title,
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-1,
            xanchor="center",
            x=0.5,
            font=dict(size=10),
            bgcolor="rgba(0,0,0,0)"
        ) if show_legend else None,
        height=450 if show_legend else 250,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig