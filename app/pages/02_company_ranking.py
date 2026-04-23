import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_all_data
from utils.scoring import prepare_companies_df
from utils.i18n import render_language_selector, t, get_lang, translate_tech_route, translate_signal_type

lang = get_lang()
st.set_page_config(page_title=t("page_title_ranking"), layout="wide")
render_language_selector()

st.title(t("title_ranking"))

data = load_all_data()
companies_df = data.get('companies', pd.DataFrame())

if not companies_df.empty:
    companies_df = prepare_companies_df(companies_df)

    tech_routes_raw = companies_df['tech_route'].dropna().unique().tolist()
    tech_routes_display = [t("all")] + sorted([translate_tech_route(r) for r in tech_routes_raw])
    tech_filter_display = st.selectbox(t("tech_filter_label"), tech_routes_display, key=f"rank_route_{lang}")

    if tech_filter_display != t("all"):
        reverse_tech = {translate_tech_route(r): r for r in tech_routes_raw}
        filter_raw = reverse_tech.get(tech_filter_display, tech_filter_display)
        companies_df = companies_df[companies_df['tech_route'] == filter_raw]

    # 翻译显示列名
    display_cols = {
        'company_name': 'Company' if lang == 'en' else '公司',
        'en_name': 'EN Name' if lang == 'en' else '英文名',
        'tech_route': 'Tech Route' if lang == 'en' else '技术路线',
        'total_score': 'Overall' if lang == 'en' else '综合评分',
        'funding_score': 'Funding' if lang == 'en' else '融资评分',
        'paper_score': 'Academic' if lang == 'en' else '学术评分',
        'signal_type': 'Signal' if lang == 'en' else '信号类型',
    }
    df_display = companies_df[list(display_cols.keys())].copy()
    df_display['tech_route'] = df_display['tech_route'].apply(translate_tech_route)
    df_display['signal_type'] = df_display['signal_type'].apply(translate_signal_type)
    df_display.columns = list(display_cols.values())

    st.dataframe(df_display.sort_values(display_cols['total_score'], ascending=False), use_container_width=True)

    top5 = companies_df.nlargest(5, 'total_score')
    import plotly.graph_objects as go
    categories = [t("radar_funding"), t("radar_academic"), t("radar_patent"), t("radar_opensource"), t("radar_hiring")]
    fig = go.Figure()
    for _, row in top5.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row['funding_score'], row['paper_score'], row['patent_score'], row['opensource_score'], row['hiring_score']],
            theta=categories,
            fill='toself',
            name=row['company_name']
        ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])), showlegend=True, title=t("radar_title"))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning(t("no_company_data"))
