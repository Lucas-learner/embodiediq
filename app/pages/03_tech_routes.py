import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_all_data
from utils.i18n import render_language_selector, t, translate_tech_route

st.set_page_config(page_title=t("page_title_tech"), layout="wide")
render_language_selector()

st.title(t("title_tech"))

data = load_all_data()
papers_df = data.get('papers', pd.DataFrame())
companies_df = data.get('companies', pd.DataFrame())

if not papers_df.empty and 'tech_route' in papers_df.columns:
    route_counts = papers_df['tech_route'].value_counts()
    route_labels = [translate_tech_route(r) for r in route_counts.index]
    fig1 = px.bar(
        x=route_labels, y=route_counts.values,
        title=t("paper_dist_title"),
        labels={'x': t("paper_dist_x"), 'y': t("paper_dist_y")}
    )
    st.plotly_chart(fig1, use_container_width=True)

    papers_df['published'] = pd.to_datetime(papers_df['published'])
    papers_df['year_month'] = papers_df['published'].dt.to_period('M').astype(str)
    trend = papers_df.groupby(['year_month', 'tech_route']).size().reset_index(name='count')
    trend['tech_route'] = trend['tech_route'].apply(translate_tech_route)
    fig2 = px.line(
        trend, x='year_month', y='count', color='tech_route',
        title=t("trend_title")
    )
    st.plotly_chart(fig2, use_container_width=True)

    if not companies_df.empty and 'tech_route' in companies_df.columns:
        st.subheader(t("company_section"))
        company_routes = companies_df['tech_route'].value_counts()
        company_labels = [translate_tech_route(r) for r in company_routes.index]
        fig3 = px.pie(
            values=company_routes.values, names=company_labels,
            title=t("company_pie_title")
        )
        st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning(t("no_topic_data"))
