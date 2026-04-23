import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_all_data
from utils.scoring import prepare_companies_df
from utils.i18n import render_language_selector, t, translate_tech_route

st.set_page_config(page_title=t("page_title_compare"), layout="wide")
render_language_selector()

st.title(t("title_compare"))

data = load_all_data()
companies_df = data.get('companies', pd.DataFrame())

if not companies_df.empty:
    companies_df = prepare_companies_df(companies_df)
    company_list = sorted(companies_df['company_name'].tolist())

    col1, col2 = st.columns(2)
    with col1:
        c1 = st.selectbox(t("select_company_a"), company_list, index=0)
    with col2:
        c2 = st.selectbox(t("select_company_b"), company_list, index=min(1, len(company_list)-1))

    if c1 and c2 and c1 != c2:
        row1 = companies_df[companies_df['company_name'] == c1].iloc[0]
        row2 = companies_df[companies_df['company_name'] == c2].iloc[0]

        categories = [t("radar_funding"), t("radar_academic"), t("radar_patent"), t("radar_opensource"), t("radar_hiring")]
        fig = go.Figure()
        fig.add_trace(go.Bar(name=c1, x=categories, y=[
            row1['funding_score'], row1['paper_score'], row1['patent_score'], row1['opensource_score'], row1['hiring_score']
        ]))
        fig.add_trace(go.Bar(name=c2, x=categories, y=[
            row2['funding_score'], row2['paper_score'], row2['patent_score'], row2['opensource_score'], row2['hiring_score']
        ]))
        fig.update_layout(barmode='group', title=t("chart_title_compare").format(c1=c1, c2=c2))
        st.plotly_chart(fig, use_container_width=True)

        compare_df = pd.DataFrame({
            t("compare_metric"): [
                t("compare_tech_route"), t("compare_funding_round"), t("compare_funding_amount"),
                t("compare_papers"), t("compare_patents"), t("compare_stars"), t("compare_score")
            ],
            c1: [
                translate_tech_route(row1['tech_route']), row1['funding_round'], row1['amount_rmb_m'],
                row1['paper_count_12m'], row1['patent_count_12m'], row1['github_stars'], row1['total_score']
            ],
            c2: [
                translate_tech_route(row2['tech_route']), row2['funding_round'], row2['amount_rmb_m'],
                row2['paper_count_12m'], row2['patent_count_12m'], row2['github_stars'], row2['total_score']
            ]
        })
        st.dataframe(compare_df.astype(str), use_container_width=True)
    else:
        st.info(t("select_diff_hint"))
else:
    st.warning(t("no_company_data"))
