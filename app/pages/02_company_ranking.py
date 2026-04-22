import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_all_data
from utils.scoring import prepare_companies_df

st.set_page_config(page_title="公司排行 | EmbodiedIQ", layout="wide")
st.title("🏆 公司活跃度排行")

data = load_all_data()
companies_df = data.get('companies', pd.DataFrame())

if not companies_df.empty:
    companies_df = prepare_companies_df(companies_df)
    
    tech_filter = st.selectbox("技术路线筛选", ['全部'] + sorted(companies_df['tech_route'].dropna().unique().tolist()))
    if tech_filter != '全部':
        companies_df = companies_df[companies_df['tech_route'] == tech_filter]
    
    st.dataframe(
        companies_df[['company_name','en_name','tech_route','total_score','funding_score','paper_score','signal_type']].sort_values('total_score', ascending=False),
        use_container_width=True
    )
    
    # 雷达图展示Top5
    top5 = companies_df.nlargest(5, 'total_score')
    import plotly.graph_objects as go
    categories = ['融资','学术','专利','开源','招聘']
    fig = go.Figure()
    for _, row in top5.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row['funding_score'], row['paper_score'], row['patent_score'], row['opensource_score'], row['hiring_score']],
            theta=categories,
            fill='toself',
            name=row['company_name']
        ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])), showlegend=True, title="Top5 公司五维评分雷达图")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("暂无公司数据")
