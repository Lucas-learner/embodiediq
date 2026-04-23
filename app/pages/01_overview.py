import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_all_data
from utils.i18n import render_language_selector, t, translate_tech_route

st.set_page_config(page_title=t("page_title_overview"), layout="wide")
render_language_selector()

st.title(t("title_overview"))
st.markdown(t("subtitle_overview"))

data = load_all_data()
papers_df = data.get('papers', pd.DataFrame())
funding_df = data.get('funding', pd.DataFrame())
companies_df = data.get('companies', pd.DataFrame())

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(t("metric_total_companies"), len(companies_df['company_name'].unique()) if not companies_df.empty else 0)
with col2:
    st.metric(t("metric_total_papers"), len(papers_df))
with col3:
    st.metric(t("metric_total_funding"), len(funding_df))

if not papers_df.empty and 'published' in papers_df.columns:
    papers_df['published'] = pd.to_datetime(papers_df['published'])
    monthly = papers_df.groupby(papers_df['published'].dt.to_period('M')).size().reset_index(name='count')
    monthly['published'] = monthly['published'].astype(str)
    fig = px.bar(
        monthly, x='published', y='count',
        title=t("paper_trend_chart_title"),
        labels={'published': t("paper_trend_xlabel"), 'count': t("paper_trend_ylabel")}
    )
    st.plotly_chart(fig, use_container_width=True)

if not funding_df.empty and 'funding_date' in funding_df.columns:
    funding_df['funding_date'] = pd.to_datetime(funding_df['funding_date'])
    monthly_f = funding_df.groupby(funding_df['funding_date'].dt.to_period('M'))['amount_rmb_m'].sum().reset_index()
    monthly_f['funding_date'] = monthly_f['funding_date'].astype(str)
    fig2 = px.line(
        monthly_f, x='funding_date', y='amount_rmb_m',
        title=t("funding_trend_chart_title"),
        labels={'funding_date': t("funding_trend_xlabel"), 'amount_rmb_m': t("funding_trend_ylabel")}
    )
    st.plotly_chart(fig2, use_container_width=True)

if not papers_df.empty and 'tech_route' in papers_df.columns:
    route_counts = papers_df['tech_route'].value_counts().head(8)
    route_labels = [translate_tech_route(r) for r in route_counts.index]
    fig3 = px.pie(
        values=route_counts.values, names=route_labels,
        title=t("tech_route_pie_title")
    )
    st.plotly_chart(fig3, use_container_width=True)
