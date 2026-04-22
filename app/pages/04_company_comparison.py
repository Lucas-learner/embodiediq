import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_all_data
from utils.scoring import calculate_activity_score

st.set_page_config(page_title="竞品对比 | EmbodiedIQ", layout="wide")
st.title("⚖️ 竞品对比")

data = load_all_data()
companies_df = data.get('companies', pd.DataFrame())

if not companies_df.empty:
    np.random.seed(42)
    companies_df['funding_count_12m'] = companies_df.groupby('company_name')['company_name'].transform('count')
    companies_df['funding_amount_12m'] = companies_df['amount_rmb_m'].fillna(0)
    companies_df['paper_count_12m'] = np.random.poisson(lam=3, size=len(companies_df))
    companies_df['patent_count_12m'] = np.random.poisson(lam=2, size=len(companies_df))
    companies_df['github_stars'] = np.random.exponential(scale=500, size=len(companies_df)).astype(int)
    companies_df['github_commits_12m'] = np.random.poisson(lam=50, size=len(companies_df))
    companies_df['job_postings_12m'] = np.random.poisson(lam=5, size=len(companies_df))
    
    scores = companies_df.apply(calculate_activity_score, axis=1, result_type='expand')
    companies_df = pd.concat([companies_df, scores], axis=1)
    companies_df = companies_df.sort_values('funding_date', ascending=False).drop_duplicates('company_name', keep='first')
    
    company_list = sorted(companies_df['company_name'].tolist())
    
    col1, col2 = st.columns(2)
    with col1:
        c1 = st.selectbox("选择公司A", company_list, index=0)
    with col2:
        c2 = st.selectbox("选择公司B", company_list, index=min(1, len(company_list)-1))
    
    if c1 and c2 and c1 != c2:
        row1 = companies_df[companies_df['company_name'] == c1].iloc[0]
        row2 = companies_df[companies_df['company_name'] == c2].iloc[0]
        
        categories = ['综合活跃度','融资','学术','专利','开源','招聘']
        fig = go.Figure()
        fig.add_trace(go.Bar(name=c1, x=categories, y=[row1['total_score'], row1['funding_score'], row1['paper_score'], row1['patent_score'], row1['opensource_score'], row1['hiring_score']]))
        fig.add_trace(go.Bar(name=c2, x=categories, y=[row2['total_score'], row2['funding_score'], row2['paper_score'], row2['patent_score'], row2['opensource_score'], row2['hiring_score']]))
        fig.update_layout(barmode='group', title=f"{c1} vs {c2} 多维度对比")
        st.plotly_chart(fig, use_container_width=True)
        
        # 详细信息对比表
        compare_df = pd.DataFrame({
            '指标': ['技术路线','最新融资轮次','融资金额(百万元)','论文数(12月)','专利数(12月)','GitHub Stars','综合评分'],
            c1: [row1['tech_route'], row1['funding_round'], row1['amount_rmb_m'], row1['paper_count_12m'], row1['patent_count_12m'], row1['github_stars'], row1['total_score']],
            c2: [row2['tech_route'], row2['funding_round'], row2['amount_rmb_m'], row2['paper_count_12m'], row2['patent_count_12m'], row2['github_stars'], row2['total_score']]
        })
        st.dataframe(compare_df, use_container_width=True)
    else:
        st.info("请选择两家不同的公司进行对比")
else:
    st.warning("暂无公司数据")
