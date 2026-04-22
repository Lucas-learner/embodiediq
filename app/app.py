import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.data_loader import load_all_data
from utils.scoring import calculate_activity_score, detect_signal_type

# 页面配置
st.set_page_config(
    page_title="EmbodiedIQ | 具身智能投资雷达",
    page_icon="🤖",
    layout="wide"
)

# 自定义CSS
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

# 主标题
st.markdown('<p class="main-header">🤖 EmbodiedIQ</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">具身智能赛道投资信号雷达 | Embodied Intelligence Investment Radar</p>', unsafe_allow_html=True)
st.markdown("---")

# 加载数据
@st.cache_data
def get_data():
    return load_all_data()

try:
    data = get_data()
    companies_df = data['companies'].copy()
    papers_df = data['papers'].copy()
    funding_df = data['funding'].copy()
    
    # 为公司数据生成模拟信号字段（MVP阶段，后续替换为真实数据）
    np.random.seed(42)
    companies_df['funding_count_12m'] = companies_df.groupby('company_name')['company_name'].transform('count')
    companies_df['funding_amount_12m'] = companies_df['amount_rmb_m'].fillna(0)
    companies_df['paper_count_12m'] = np.random.poisson(lam=3, size=len(companies_df))
    companies_df['patent_count_12m'] = np.random.poisson(lam=2, size=len(companies_df))
    companies_df['github_stars'] = np.random.exponential(scale=500, size=len(companies_df)).astype(int)
    companies_df['github_commits_12m'] = np.random.poisson(lam=50, size=len(companies_df))
    companies_df['job_postings_12m'] = np.random.poisson(lam=5, size=len(companies_df))
    
    # 计算评分
    scores = companies_df.apply(calculate_activity_score, axis=1, result_type='expand')
    companies_df = pd.concat([companies_df, scores], axis=1)
    companies_df['signal_type'] = companies_df.apply(detect_signal_type, axis=1)
    
    # 去重：保留每家公司最新融资记录
    companies_df = companies_df.sort_values('funding_date', ascending=False).drop_duplicates('company_name', keep='first')
    
except Exception as e:
    st.error(f"数据加载失败: {e}")
    st.info("请确保数据文件已准备就绪。首次使用可参考README准备数据。")
    companies_df = pd.DataFrame()
    papers_df = pd.DataFrame()
    funding_df = pd.DataFrame()

# 侧边栏
with st.sidebar:
    st.header("⚙️ 筛选器")
    
    if not companies_df.empty:
        # 技术路线筛选
        tech_routes = ['全部'] + sorted(companies_df['tech_route'].dropna().unique().tolist())
        selected_route = st.selectbox("技术路线", tech_routes)
        
        # 时间范围
        time_range = st.selectbox("时间范围", ["全部", "最近6个月", "最近12个月", "2025年", "2024年"])
        
        # 活跃度排序
        sort_by = st.selectbox("排序方式", ["综合活跃度", "融资活跃度", "学术活跃度", "开源活跃度"])
    
    st.markdown("---")
    st.markdown("**关于**")
    st.markdown("EmbodiedIQ整合融资、学术、专利、开源多维信号，辅助具身智能赛道投资决策。")

# 应用筛选
display_df = companies_df.copy() if not companies_df.empty else pd.DataFrame()

if not companies_df.empty:
    
    if selected_route != '全部':
        display_df = display_df[display_df['tech_route'] == selected_route]
    
    # 时间筛选（简化处理）
    if time_range == "2025年":
        display_df = display_df[display_df['funding_date'].astype(str).str.startswith('2025')]
    elif time_range == "2024年":
        display_df = display_df[display_df['funding_date'].astype(str).str.startswith('2024')]
    
    # 排序
    sort_map = {
        "综合活跃度": "total_score",
        "融资活跃度": "funding_score",
        "学术活跃度": "paper_score",
        "开源活跃度": "opensource_score"
    }
    display_df = display_df.sort_values(sort_map.get(sort_by, "total_score"), ascending=False)

# 核心指标卡片
if not companies_df.empty:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 覆盖公司", len(companies_df))
    with col2:
        st.metric("📄 论文追踪", len(papers_df) if not papers_df.empty else 0)
    with col3:
        st.metric("💰 融资事件", len(funding_df) if not funding_df.empty else 0)
    with col4:
        high_signal = len(companies_df[companies_df['signal_type'] == 'Early_Signal'])
        st.metric("🚨 早期信号", high_signal, help="技术信号强但融资少的机会型项目")

# 主内容区分页（使用Streamlit原生方式或pages目录）
st.markdown("---")
st.info("👈 使用左侧边栏的页面导航，或访问各功能模块：")

# 展示简要数据预览
if not display_df.empty:
    st.subheader("📈 活跃度排行 Top 10")
    top10 = display_df.nlargest(10, 'total_score')[['company_name', 'en_name', 'tech_route', 'total_score', 'signal_type']]
    
    # 用颜色标记信号类型
    def color_signal(val):
        colors = {
            'Substantive_Growth': 'background-color: #d4edda',
            'Funding_Driven': 'background-color: #fff3cd', 
            'Early_Signal': 'background-color: #cce5ff',
            'Low_Activity': ''
        }
        return colors.get(val, '')
    
    st.dataframe(
        top10.style.map(color_signal, subset=['signal_type']),
        use_container_width=True
    )

    # 信号类型分布
    st.subheader("🎯 赛道信号分布")
    col1, col2 = st.columns(2)
    
    with col1:
        signal_counts = companies_df['signal_type'].value_counts()
        fig = px.pie(values=signal_counts.values, names=signal_counts.index,
                     title="信号类型分布",
                     color_discrete_map={
                         'Substantive_Growth': '#28a745',
                         'Funding_Driven': '#ffc107',
                         'Early_Signal': '#007bff',
                         'Low_Activity': '#6c757d'
                     })
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'tech_route' in companies_df.columns:
            route_counts = companies_df['tech_route'].value_counts().head(8)
            fig = px.bar(x=route_counts.index, y=route_counts.values,
                        title="技术路线分布",
                        labels={'x': '技术路线', 'y': '公司数量'})
            st.plotly_chart(fig, use_container_width=True)
    
    # 融资趋势时序图
    st.subheader("💰 融资趋势")
    if not funding_df.empty:
        funding_df['funding_date'] = pd.to_datetime(funding_df['funding_date'])
        monthly_funding = funding_df.groupby(funding_df['funding_date'].dt.to_period('M'))['amount_rmb_m'].sum().reset_index()
        monthly_funding['funding_date'] = monthly_funding['funding_date'].astype(str)
        fig = px.line(monthly_funding, x='funding_date', y='amount_rmb_m',
                     title="月度融资金额趋势（百万元人民币）",
                     labels={'funding_date': '月份', 'amount_rmb_m': '融资金额'})
        st.plotly_chart(fig, use_container_width=True)

# 论文趋势
if not papers_df.empty:
    st.subheader("📄 论文发表趋势")
    papers_df['published'] = pd.to_datetime(papers_df['published'])
    monthly_papers = papers_df.groupby(papers_df['published'].dt.to_period('M')).size().reset_index(name='count')
    monthly_papers['published'] = monthly_papers['published'].astype(str)
    fig = px.bar(monthly_papers, x='published', y='count',
                title="月度论文发表数量",
                labels={'published': '月份', 'count': '论文数量'})
    st.plotly_chart(fig, use_container_width=True)

# 页脚
st.markdown("---")
st.caption("📌 数据来源：arXiv、GitHub、IT桔子、公开报道 | 仅供投资研究方法论展示，不构成投资建议")
st.caption("Built by [你的名字] | 深圳天使投资引导基金投资研究实习生")
