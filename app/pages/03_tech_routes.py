import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_all_data

st.set_page_config(page_title="技术路线 | EmbodiedIQ", layout="wide")
st.title("🔬 技术路线竞争格局")

data = load_all_data()
papers_df = data.get('papers', pd.DataFrame())
companies_df = data.get('companies', pd.DataFrame())

if not papers_df.empty and 'tech_route' in papers_df.columns:
    # 论文技术路线分布
    route_counts = papers_df['tech_route'].value_counts()
    fig1 = px.bar(x=route_counts.index, y=route_counts.values, title="论文技术路线分布", labels={'x':'技术路线','y':'论文数量'})
    st.plotly_chart(fig1, use_container_width=True)
    
    # 技术路线时间趋势
    papers_df['published'] = pd.to_datetime(papers_df['published'])
    papers_df['year_month'] = papers_df['published'].dt.to_period('M').astype(str)
    trend = papers_df.groupby(['year_month','tech_route']).size().reset_index(name='count')
    fig2 = px.line(trend, x='year_month', y='count', color='tech_route', title="技术路线热度趋势")
    st.plotly_chart(fig2, use_container_width=True)
    
    # 技术路线与公司关联
    if not companies_df.empty and 'tech_route' in companies_df.columns:
        st.subheader("公司技术路线分布")
        company_routes = companies_df['tech_route'].value_counts()
        fig3 = px.pie(values=company_routes.values, names=company_routes.index, title="公司技术路线占比")
        st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("暂无论文主题数据，请先运行主题模型")
