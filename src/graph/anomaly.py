import pandas as pd
import numpy as np
import plotly.graph_objs as go
import streamlit as st

def plot_anomaly_line_chart(df, selected_genre=None, GENRE_COLORS=None):
    # 선택된 장르 없을 시 전체 장르 데이터 사용
    if selected_genre is None:
        df_g = df
    else:
        df_g = df[df['genres'].isin(selected_genre)]

    fig = go.Figure()

    for genre, group in df_g.groupby('genres'):
        fig.add_trace(go.Scatter(
            x=group['week_block'],
            y=group['weekly_user'],
            mode='lines',
            line=dict(color=GENRE_COLORS[genre]) if GENRE_COLORS else None,
            name=genre,
            hoverinfo='text',
            showlegend=False if GENRE_COLORS else True,
            text=[f"{genre}<br>주차: {w}<br>유저수: {u}" for w, u in zip(group['week_block'], group['weekly_user'])]
        ))

    anomalies = df_g[df_g['anomaly']]
    fig.add_trace(go.Scatter(
        x=anomalies['week_block'],
        y=anomalies['weekly_user'],
        mode='markers',
        name='이상값',
        marker=dict(color='red', size=10, symbol='circle-open'),
        text=[f"{row['genres']}<br>주차: {row['week_block']}<br>유저수: {row['weekly_user']}" for _, row in anomalies.iterrows()],
        hovertemplate='%{text}<extra></extra>',
        showlegend=True
    ))

    fig.update_layout(
        title="장르별 주간 전체 유저수 및 이상값",
        xaxis_title="주차",
        yaxis_title="주간 전체 유저수",
        legend=dict(title='장르'),
        hovermode='closest',
        height=600
    )
    return fig