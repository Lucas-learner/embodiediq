import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_all_data

st.set_page_config(page_title="赛道总览 | EmbodiedIQ", layout="wide")
st.title("📊 赛道总览")
st.markdown("具身智能赛道多维度信号监控")

data = load_all_data()
papers_df = data.get('papers', pd.DataFrame())
funding_df = data.get('funding', pd.DataFrame())
companies_df = data.get('companies', pd.DataFrame())

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("覆盖公司", len(companies_df['company_name'].unique()) if not companies_df.empty else 0)
with col2:
    st.metric("论文总数", len(papers_df))
with col3:
    st.metric("融资事件", len(funding_df))

# 论文趋势
if not papers_df.empty and 'published' in papers_df.columns:
    papers_df['published'] = pd.to_datetime(papers_df['published'])
    monthly = papers_df.groupby(papers_df['published'].dt.to_period('M')).size().reset_index(name='count')
    monthly['published'] = monthly['published'].astype(str)
    fig = px.bar(monthly, x='published', y='count', title="论文发表趋势", labels={'published':'月份','count':'数量'})
    st.plotly_chart(fig, use_container_width=True)

# 融资趋势
if not funding_df.empty and 'funding_date' in funding_df.columns:
    funding_df['funding_date'] = pd.to_datetime(funding_df['funding_date'])
    monthly_f = funding_df.groupby(funding_df['funding_date'].dt.to_period('M'))['amount_rmb_m'].sum().reset_index()
    monthly_f['funding_date'] = monthly_f['funding_date'].astype(str)
    fig2 = px.line(monthly_f, x='funding_date', y='amount_rmb_m', title="融资趋势（百万元）", labels={'funding_date':'月份','amount_rmb_m':'金额'})
    st.plotly_chart(fig2, use_container_width=True)

# 技术路线分布
if not papers_df.empty and 'tech_route' in papers_df.columns:
    route_counts = papers_df['tech_route'].value_counts().head(8)
    fig3 = px.pie(values=route_counts.values, names=route_counts.index, title="论文技术路线分布")
    st.plotly_chart(fig3, use_container_width=True)
