import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.data_loader import load_all_data
from utils.scoring import prepare_companies_df
from utils.i18n import render_language_selector, t, get_lang, translate_signal_type, translate_tech_route

lang = get_lang()

st.set_page_config(
    page_title=t("page_title_main"),
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #1f1f1f;
}
.sub-header {
    font-size: 1.2rem;
    color: #666;
}
.metric-card {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🤖 EmbodiedIQ</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header">{t("sub_header")}</p>', unsafe_allow_html=True)
st.markdown("---")

@st.cache_data
def get_data():
    return load_all_data()

try:
    data = get_data()
    companies_df = data['companies'].copy()
    papers_df = data['papers'].copy()
    funding_df = data['funding'].copy()
    companies_df = prepare_companies_df(companies_df)
except Exception as e:
    st.error(t("data_load_error").format(e=e))
    st.info(t("data_load_hint"))
    companies_df = pd.DataFrame()
    papers_df = pd.DataFrame()
    funding_df = pd.DataFrame()

with st.sidebar:
    render_language_selector()
    st.header(t("sidebar_filter"))

    if not companies_df.empty:
        tech_routes_raw = companies_df['tech_route'].dropna().unique().tolist()
        tech_routes_display = [t("all")] + sorted([translate_tech_route(r) for r in tech_routes_raw])
        selected_route_display = st.selectbox(t("tech_route_label"), tech_routes_display, key=f"route_{lang}")

        time_options = [t("time_all"), t("time_6m"), t("time_12m"), t("time_2025"), t("time_2024")]
        time_range = st.selectbox(t("time_range_label"), time_options, key=f"time_{lang}")

        sort_options = [t("sort_overall"), t("sort_funding"), t("sort_academic"), t("sort_opensource")]
        sort_by = st.selectbox(t("sort_by_label"), sort_options, key=f"sort_{lang}")

    st.markdown("---")
    st.markdown(f"**{t('about')}**")
    st.markdown(t("about_text"))

display_df = companies_df.copy() if not companies_df.empty else pd.DataFrame()

if not companies_df.empty:
    if selected_route_display != t("all"):
        # 将显示值反向映射回原始值进行筛选
        reverse_tech = {translate_tech_route(r): r for r in tech_routes_raw}
        selected_route_raw = reverse_tech.get(selected_route_display, selected_route_display)
        display_df = display_df[display_df['tech_route'] == selected_route_raw]

    if time_range == t("time_2025"):
        display_df = display_df[display_df['funding_date'].astype(str).str.startswith('2025')]
    elif time_range == t("time_2024"):
        display_df = display_df[display_df['funding_date'].astype(str).str.startswith('2024')]

    sort_map = {
        t("sort_overall"): "total_score",
        t("sort_funding"): "funding_score",
        t("sort_academic"): "paper_score",
        t("sort_opensource"): "opensource_score"
    }
    display_df = display_df.sort_values(sort_map.get(sort_by, "total_score"), ascending=False)

if not companies_df.empty:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(t("metric_companies"), len(companies_df))
    with col2:
        st.metric(t("metric_papers"), len(papers_df) if not papers_df.empty else 0)
    with col3:
        st.metric(t("metric_funding"), len(funding_df) if not funding_df.empty else 0)
    with col4:
        high_signal = len(companies_df[companies_df['signal_type'] == 'Early_Signal'])
        st.metric(t("metric_early_signal"), high_signal, help=t("metric_early_help"))

st.markdown("---")
st.info(t("nav_hint"))

if not display_df.empty:
    st.subheader(t("top10_title"))
    top10 = display_df.nlargest(10, 'total_score')[['company_name', 'en_name', 'tech_route', 'total_score', 'signal_type']].copy()

    # 翻译显示列
    top10['tech_route'] = top10['tech_route'].apply(translate_tech_route)
    top10['signal_type'] = top10['signal_type'].apply(translate_signal_type)

    def color_signal(val):
        colors = {
            translate_signal_type('Substantive_Growth'): 'background-color: #d4edda',
            translate_signal_type('Funding_Driven'): 'background-color: #fff3cd',
            translate_signal_type('Early_Signal'): 'background-color: #cce5ff',
            translate_signal_type('Low_Activity'): ''
        }
        return colors.get(val, '')

    st.dataframe(
        top10.style.map(color_signal, subset=['signal_type']),
        use_container_width=True
    )

    st.subheader(t("signal_distribution"))
    col1, col2 = st.columns(2)

    with col1:
        signal_counts = companies_df['signal_type'].value_counts()
        signal_labels = [translate_signal_type(s) for s in signal_counts.index]
        fig = px.pie(
            values=signal_counts.values,
            names=signal_labels,
            title=t("signal_type_pie_title"),
            color_discrete_map={
                translate_signal_type('Substantive_Growth'): '#28a745',
                translate_signal_type('Funding_Driven'): '#ffc107',
                translate_signal_type('Early_Signal'): '#007bff',
                translate_signal_type('Low_Activity'): '#6c757d'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        if 'tech_route' in companies_df.columns:
            route_counts = companies_df['tech_route'].value_counts().head(8)
            route_labels = [translate_tech_route(r) for r in route_counts.index]
            fig = px.bar(
                x=route_labels,
                y=route_counts.values,
                title=t("tech_route_bar_title"),
                labels={'x': t("tech_route_x"), 'y': t("tech_route_y")}
            )
            st.plotly_chart(fig, use_container_width=True)

    st.subheader(t("funding_trend_title"))
    if not funding_df.empty:
        funding_df['funding_date'] = pd.to_datetime(funding_df['funding_date'])
        monthly_funding = funding_df.groupby(funding_df['funding_date'].dt.to_period('M'))['amount_rmb_m'].sum().reset_index()
        monthly_funding['funding_date'] = monthly_funding['funding_date'].astype(str)
        fig = px.line(
            monthly_funding,
            x='funding_date',
            y='amount_rmb_m',
            title=t("funding_monthly_title"),
            labels={'funding_date': t("funding_month_x"), 'amount_rmb_m': t("funding_amount_y")}
        )
        st.plotly_chart(fig, use_container_width=True)

if not papers_df.empty:
    st.subheader(t("paper_trend_title"))
    papers_df['published'] = pd.to_datetime(papers_df['published'])
    monthly_papers = papers_df.groupby(papers_df['published'].dt.to_period('M')).size().reset_index(name='count')
    monthly_papers['published'] = monthly_papers['published'].astype(str)
    fig = px.bar(
        monthly_papers,
        x='published',
        y='count',
        title=t("paper_monthly_title"),
        labels={'published': t("paper_month_x"), 'count': t("paper_count_y")}
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption(t("footer_source"))
st.caption(t("footer_author"))
