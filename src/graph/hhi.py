import pandas as pd
import numpy as np
import plotly.graph_objs as go
import streamlit as st
import plotly.express as px
import colorsys

def generate_color_map(base_hex: str, n: int) -> list:
    """기본 HEX 색상으로부터 밝기를 변화시켜 n개의 색상 생성"""
    base_hex = base_hex.lstrip("#")
    r, g, b = [int(base_hex[i:i+2], 16)/255.0 for i in (0, 2, 4)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # 밝기 l 기준으로 선형 분포로 변화 (밝게 -> 어둡게)
    l_range = [max(0, min(1, l * (1.2 - i * 0.8 / max(n-1, 1)))) for i in range(n)]

    colors = []
    for l_val in l_range:
        r_i, g_i, b_i = colorsys.hls_to_rgb(h, l_val, s)
        rgb_str = f"rgb({int(r_i*255)}, {int(g_i*255)}, {int(b_i*255)})"
        colors.append(rgb_str)
    
    return colors

def plot_hhi_line_chart(df, selected_genre=None, GENRE_COLORS=None):
    if selected_genre is None:
        df_g = df
    else:
        df_g = df[df['genres'].isin(selected_genre)]

    total_user_per_week = df.groupby('week_block')['weekly_user'].sum().rename('total_user')
    df = df.merge(total_user_per_week, on='week_block')
    
    fig = go.Figure()
    for genre in df_g['genres'].unique():
        tmp = df_g[df_g['genres'] == genre]
        fig.add_trace(go.Scatter(
            x=tmp['week_block'],
            y=tmp['hhi_rolling'],
            mode='lines',
            line=dict(color=GENRE_COLORS[genre]) if GENRE_COLORS else None,
            name=genre))
    fig.update_layout(title='HHI Trend by Genre', xaxis_title='Week', yaxis_title='HHI', legend_title='Genre')
    return fig

def plot_stacked_bar_chart(df, GENRE_COLORS=None, selected_genre=None):
    """
    selected_genre 가 None
        x축: 장르, y축: 평균 monthly_user
        Top-5 게임 + Others 를 스택, 점유율 낮을수록 opacity ↑(진한색)
    selected_genre 가 지정된 경우
        x축: 월, y축: 유저 수
        장르별 offset group 으로 월별 스택
    """
    # -------- 1) 전체 장르 모드 --------
    if selected_genre is None:
        df = df[df['name'] != 'Others']
        agg = (
            df.groupby(['genres', 'name'])['monthly_user']
              .mean()
              .reset_index()
        )

        fig = go.Figure()
        for genre in agg['genres'].unique():
            
            g_df = agg[agg['genres'] == genre].sort_values('monthly_user', ascending=False).reset_index(drop=True)
            total = g_df['monthly_user'].sum()

            base_hex = GENRE_COLORS.get(genre, '#333333')
            n = len(g_df)
            color_map = generate_color_map(base_hex, n)

            for i, row in g_df.iterrows():
                name, val = row['name'], row['monthly_user']
                share = val / total if total else 0
                perc = share * 100

                color = 'rgba(200,200,200,1)' if name.lower() == 'others' else color_map[i]

                fig.add_trace(go.Bar(
                    x=[genre],
                    y=[perc],
                    name=name,
                    marker_color=color,
                    hovertemplate=f"{name}: {{y:.1f}}%<extra></extra>",
                    showlegend=False  # 장르별로 많은 게임 있으니 범례는 생략하거나 조건부 사용
                ))

        fig.update_layout(
            barmode='stack',
            title='장르별 점유율 상위 게임 (%)',
            xaxis_title='장르',
            yaxis_title='점유율(%)',
            yaxis_tickformat='.0f',
            legend_title='게임'
        )
        return fig

    # -------- 2) 선택 장르 모드 --------
    
    months = sorted(df['month_block'].unique())
    palette = px.colors.qualitative.Pastel + px.colors.qualitative.Set2   # 더 부드러운 색
    palette = [c for c in palette if c.lower() not in {'#ffffff', 'white'}]

    color_cycle = iter(palette)
    color_map = {}

    fig = go.Figure()
    names = list(df[df['genres'] == selected_genre]['name'].unique())
    names_sorted = [name for name in names if name != 'Others']
    names_sorted.sort()
    # names_sorted = ['Others'] + names_sorted

    for name in names_sorted:
        if name not in color_map:
            color_map[name] = next(color_cycle)
        vals = [
            df.loc[(df['month_block'] == m) & (df['name'] == name), 'monthly_user'].sum()
            if m in df['month_block'].values else 0
            for m in months
        ]
        fig.add_trace(go.Bar(
            x=months, y=vals, name=name,
            marker_color=color_map[name],
            offsetgroup=selected_genre, legendgroup=name,
            hovertemplate=f"{name}: %{{y}}<extra></extra>"
        ))

    fig.update_layout(
        barmode='stack',
        title='선택 장르 게임별 월간 유저수',
        xaxis_title='월',
        yaxis_title='유저수',
        legend_title='게임',
        bargap=0.25    # 장르별 간격 확보
    )
    return fig