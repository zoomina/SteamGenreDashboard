import pandas as pd
import numpy as np
import plotly.graph_objs as go
import streamlit as st
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from tslearn.metrics import cdist_dtw
from tslearn.barycenters import dtw_barycenter_averaging
from sklearn_extra.cluster import KMedoids
import plotly.express as px

def plot_cluster_trend_feature(df, selected_genre=None):
    if selected_genre is None:
        selected_genre = df['genres'].dropna().unique()
    df = df[df['genres'].isin(selected_genre)]

    pivot = df.groupby(['genres', 'month']).monthly_user.sum().unstack(fill_value=0)
    genres = pivot.index

    # z-score 정규화
    scaler = TimeSeriesScalerMeanVariance()
    X = scaler.fit_transform(pivot.values)

    # x축: 추세(선형 회귀 기울기)
    trend = [np.polyfit(np.arange(len(x)), x, 1)[0] for x in X.squeeze()]

    # y축: peak timing (최대값 위치, 0~1로 정규화)
    peak_timing = [np.argmax(x) / (len(x)-1) for x in X.squeeze()]

    dtw_dist = cdist_dtw(X)
    n_clusters = 3  # 원하는 군집 수
    kmedoids = KMedoids(n_clusters=n_clusters, metric='precomputed', random_state=0).fit(dtw_dist)
    labels = kmedoids.labels_

    return genres, trend, peak_timing, labels, X

def plot_cluster_trend_scatter(genres, trend, peak_timing, labels):
    df_plot = pd.DataFrame({
        'genre': genres,
        'trend': trend,
        'peak_timing': peak_timing,
        'cluster': labels
    })
    fig = px.scatter(
        df_plot, x='trend', y='peak_timing',
        color='cluster', color_discrete_sequence=['blue', 'red', 'green'],
        text='genre', title='장르별 트렌드(기울기) vs Peak Timing 기반 클러스터링',
        labels={'trend': '상승/하락 추세(기울기)', 'peak_timing': 'Peak Timing(0~1)'}
    )
    fig.update_traces(textposition='top center')
    return fig

def plot_cluster_barycenter_with_trendline(labels, X, n_clusters=3):
    fig = go.Figure()
    for c in range(n_clusters):
        idx = np.where(labels == c)[0]
        bary = dtw_barycenter_averaging(X[idx])
        bary_flat = bary.ravel()
        x_vals = np.arange(len(bary_flat))
        # 추세선(선형 회귀) 계산
        trend_coef = np.polyfit(x_vals, bary_flat, 1)
        trend_line = np.polyval(trend_coef, x_vals)
        # barycenter 곡선 추가
        fig.add_trace(go.Scatter(
            y=bary_flat,
            x=x_vals,
            mode='lines',
            name=f'Cluster {c} barycenter'
        ))
        # 추세선 추가
        fig.add_trace(go.Scatter(
            y=trend_line,
            x=x_vals,
            mode='lines',
            name=f'Cluster {c} Trend',
            line=dict(dash='dash'),
            showlegend=True
        ))
    fig.update_layout(title='클러스터별 DTW barycenter(평균 패턴) 및 추세선')
    return fig
