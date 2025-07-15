import pandas as pd
import numpy as np
import plotly.express as px

def weekday_hourly_heatmap(df, genre=None):
    
    # 정규화
    genre_total = df['weekday_user_count'].sum()
    df['norm_user'] = df['weekday_user_count'] / genre_total

    # 요일 이름 매핑
    weekday_map = {0: '일', 1: '월', 2: '화', 3: '수', 4: '목', 5: '금', 6: '토'}
    df['weekday_name'] = df['weekday'].map(weekday_map)

    # 히트맵
    fig = px.density_heatmap(
        df,
        x='hour',
        y='weekday_name',
        z='norm_user',
        color_continuous_scale='Blues',
        labels={'hour': '시간', 'weekday_name': '요일', 'norm_user': '정규화 유저수'},
        title=f'{genre} 장르의 요일-시간대 정규화 유저수 히트맵'
    )
    
    # 축 설정
    fig.update_xaxes(dtick=1)
    fig.update_yaxes(categoryorder='array', categoryarray=['일', '월', '화', '수', '목', '금', '토'])
    fig.update_layout(coloraxis_colorbar=dict(title="정규화 유저수"))
    
    return fig

def weekday_heatmap(df, selected_genre=None):
    # 선택된 장르 없을 시 전체 장르 데이터 사용
    if selected_genre is None:
        selected_genre = df['genres'].dropna().unique()
    
    df_g = df[df['genres'].isin(selected_genre)]

    grouped = df_g.groupby(['weekday', 'genres'])['weekday_user_count'].sum().reset_index()
    pivot = grouped.pivot(index='weekday', columns='genres', values='weekday_user_count').fillna(0)

    genre_totals = pivot.sum(axis=0)
    pivot_percentage = pivot.div(genre_totals, axis=1) * 100

    weekday_map = {1: '월', 2: '화', 3: '수', 4: '목', 5: '금', 6: '토', 0: '일'}
    pivot_percentage.index = pivot_percentage.index.map(weekday_map)

    fig = px.imshow(
        pivot_percentage,
        labels=dict(x="장르", y="요일", color="비율 (%)"),
        x=pivot_percentage.columns,
        y=pivot_percentage.index,
        color_continuous_scale='Blues',
        text_auto='.1f'
    )
    fig.update_layout(
        title="요일별 Active User 비율 (장르 전체 100%)",
        xaxis_title="장르",
        yaxis_title="요일",
        yaxis_autorange="reversed"
    )

    return fig

def hourly_heatmap(df, selected_genre=None):
    # 선택된 장르 없을 시 전체 장르 데이터 사용
    if selected_genre is None:
        selected_genre = df['genres'].dropna().unique()
    
    df_g = df[df['genres'].isin(selected_genre)]

    grouped = df_g.groupby(['hour', 'genres'])['hour_user_count'].sum().reset_index()
    pivot = grouped.pivot(index='hour', columns='genres', values='hour_user_count').fillna(0)

    # 4. 장르별 전체 유저 수로 비율 계산
    genre_totals = pivot.sum(axis=0)
    pivot_percentage = pivot.div(genre_totals, axis=1) * 100

    # 5. plotly 히트맵 그리기
    import plotly.express as px

    fig = px.imshow(
        pivot_percentage,
        labels=dict(x="장르", y="시간대", color="비율 (%)"),
        x=pivot_percentage.columns,
        y=pivot_percentage.index,
        color_continuous_scale='Blues',
        text_auto='.1f'
    )
    fig.update_layout(
        title="시간대별 Active User 비율 (장르 전체 100%)",
        xaxis_title="장르",
        yaxis_title="시간대 (시)",
        yaxis_autorange="reversed"
    )

    return fig