import streamlit as st

TRANSLATIONS = {
    "en": {
        # app.py
        "page_title_main": "EmbodiedIQ | Embodied Intelligence Investment Radar",
        "sub_header": "Embodied Intelligence Investment Radar",
        "data_load_error": "Data loading failed: {e}",
        "data_load_hint": "Please ensure data files are ready. Refer to README for first-time setup.",
        "sidebar_filter": "⚙️ Filters",
        "tech_route_label": "Tech Route",
        "all": "All",
        "time_range_label": "Time Range",
        "time_all": "All",
        "time_6m": "Last 6 Months",
        "time_12m": "Last 12 Months",
        "time_2025": "2025",
        "time_2024": "2024",
        "sort_by_label": "Sort By",
        "sort_overall": "Overall Activity",
        "sort_funding": "Funding Activity",
        "sort_academic": "Academic Activity",
        "sort_opensource": "Open Source Activity",
        "about": "About",
        "about_text": "EmbodiedIQ aggregates financing, academic, patent, and open-source signals to assist embodied intelligence investment decisions.",
        "metric_companies": "📊 Companies",
        "metric_papers": "📄 Papers",
        "metric_funding": "💰 Funding Events",
        "metric_early_signal": "🚨 Early Signals",
        "metric_early_help": "Projects with strong tech signals but low funding",
        "nav_hint": "👈 Use the sidebar navigation or access each module:",
        "top10_title": "📈 Top 10 Activity Ranking",
        "signal_distribution": "🎯 Signal Distribution",
        "signal_type_pie_title": "Signal Type Distribution",
        "tech_route_bar_title": "Tech Route Distribution",
        "tech_route_x": "Tech Route",
        "tech_route_y": "Company Count",
        "funding_trend_title": "💰 Funding Trend",
        "funding_monthly_title": "Monthly Funding Trend (RMB Million)",
        "funding_month_x": "Month",
        "funding_amount_y": "Funding Amount",
        "paper_trend_title": "📄 Paper Publication Trend",
        "paper_monthly_title": "Monthly Paper Count",
        "paper_month_x": "Month",
        "paper_count_y": "Paper Count",
        "footer_source": "📌 Data sources: arXiv, GitHub, IT Juzi, public reports | For research methodology demonstration only, not investment advice",
        "footer_author": "Built by Xuyang Zhang | Investment Research Intern, Shenzhen Angel Investment Guidance Fund",
        # 01_overview
        "page_title_overview": "Overview | EmbodiedIQ",
        "title_overview": "📊 Sector Overview",
        "subtitle_overview": "Multi-dimensional signal monitoring for embodied intelligence",
        "metric_total_companies": "Companies",
        "metric_total_papers": "Total Papers",
        "metric_total_funding": "Funding Events",
        "paper_trend_chart_title": "Paper Publication Trend",
        "paper_trend_xlabel": "Month",
        "paper_trend_ylabel": "Count",
        "funding_trend_chart_title": "Funding Trend (Million RMB)",
        "funding_trend_xlabel": "Month",
        "funding_trend_ylabel": "Amount",
        "tech_route_pie_title": "Paper Tech Route Distribution",
        # 02_ranking
        "page_title_ranking": "Ranking | EmbodiedIQ",
        "title_ranking": "🏆 Company Activity Ranking",
        "tech_filter_label": "Tech Route Filter",
        "radar_title": "Top 5 Company Five-Dimension Radar",
        "radar_funding": "Funding",
        "radar_academic": "Academic",
        "radar_patent": "Patent",
        "radar_opensource": "Open Source",
        "radar_hiring": "Hiring",
        "no_company_data": "No company data available",
        # 03_tech_routes
        "page_title_tech": "Tech Routes | EmbodiedIQ",
        "title_tech": "🔬 Tech Route Landscape",
        "paper_dist_title": "Paper Tech Route Distribution",
        "paper_dist_x": "Tech Route",
        "paper_dist_y": "Paper Count",
        "trend_title": "Tech Route Trend",
        "company_section": "Company Tech Route Distribution",
        "company_pie_title": "Company Tech Route Share",
        "no_topic_data": "No paper topic data available. Please run the topic model first.",
        # 04_comparison
        "page_title_compare": "Comparison | EmbodiedIQ",
        "title_compare": "⚖️ Competitor Comparison",
        "select_company_a": "Select Company A",
        "select_company_b": "Select Company B",
        "chart_title_compare": "{c1} vs {c2} Multi-Dimension Comparison",
        "compare_metric": "Metric",
        "compare_tech_route": "Tech Route",
        "compare_funding_round": "Latest Funding Round",
        "compare_funding_amount": "Funding Amount (M RMB)",
        "compare_papers": "Papers (12M)",
        "compare_patents": "Patents (12M)",
        "compare_stars": "GitHub Stars",
        "compare_score": "Overall Score",
        "select_diff_hint": "Please select two different companies to compare",
    },
    "zh": {
        # app.py
        "page_title_main": "EmbodiedIQ | 具身智能投资雷达",
        "sub_header": "具身智能赛道投资信号雷达 | Embodied Intelligence Investment Radar",
        "data_load_error": "数据加载失败: {e}",
        "data_load_hint": "请确保数据文件已准备就绪。首次使用可参考README准备数据。",
        "sidebar_filter": "⚙️ 筛选器",
        "tech_route_label": "技术路线",
        "all": "全部",
        "time_range_label": "时间范围",
        "time_all": "全部",
        "time_6m": "最近6个月",
        "time_12m": "最近12个月",
        "time_2025": "2025年",
        "time_2024": "2024年",
        "sort_by_label": "排序方式",
        "sort_overall": "综合活跃度",
        "sort_funding": "融资活跃度",
        "sort_academic": "学术活跃度",
        "sort_opensource": "开源活跃度",
        "about": "关于",
        "about_text": "EmbodiedIQ整合融资、学术、专利、开源多维信号，辅助具身智能赛道投资决策。",
        "metric_companies": "📊 覆盖公司",
        "metric_papers": "📄 论文追踪",
        "metric_funding": "💰 融资事件",
        "metric_early_signal": "🚨 早期信号",
        "metric_early_help": "技术信号强但融资少的机会型项目",
        "nav_hint": "👈 使用左侧边栏的页面导航，或访问各功能模块：",
        "top10_title": "📈 活跃度排行 Top 10",
        "signal_distribution": "🎯 赛道信号分布",
        "signal_type_pie_title": "信号类型分布",
        "tech_route_bar_title": "技术路线分布",
        "tech_route_x": "技术路线",
        "tech_route_y": "公司数量",
        "funding_trend_title": "💰 融资趋势",
        "funding_monthly_title": "月度融资金额趋势（百万元人民币）",
        "funding_month_x": "月份",
        "funding_amount_y": "融资金额",
        "paper_trend_title": "📄 论文发表趋势",
        "paper_monthly_title": "月度论文发表数量",
        "paper_month_x": "月份",
        "paper_count_y": "论文数量",
        "footer_source": "📌 数据来源：arXiv、GitHub、IT桔子、公开报道 | 仅供投资研究方法论展示，不构成投资建议",
        "footer_author": "Built by 张栩阳 | 深圳天使投资引导基金投资研究实习生",
        # 01_overview
        "page_title_overview": "赛道总览 | EmbodiedIQ",
        "title_overview": "📊 赛道总览",
        "subtitle_overview": "具身智能赛道多维度信号监控",
        "metric_total_companies": "覆盖公司",
        "metric_total_papers": "论文总数",
        "metric_total_funding": "融资事件",
        "paper_trend_chart_title": "论文发表趋势",
        "paper_trend_xlabel": "月份",
        "paper_trend_ylabel": "数量",
        "funding_trend_chart_title": "融资趋势（百万元）",
        "funding_trend_xlabel": "月份",
        "funding_trend_ylabel": "金额",
        "tech_route_pie_title": "论文技术路线分布",
        # 02_ranking
        "page_title_ranking": "公司排行 | EmbodiedIQ",
        "title_ranking": "🏆 公司活跃度排行",
        "tech_filter_label": "技术路线筛选",
        "radar_title": "Top5 公司五维评分雷达图",
        "radar_funding": "融资",
        "radar_academic": "学术",
        "radar_patent": "专利",
        "radar_opensource": "开源",
        "radar_hiring": "招聘",
        "no_company_data": "暂无公司数据",
        # 03_tech_routes
        "page_title_tech": "技术路线 | EmbodiedIQ",
        "title_tech": "🔬 技术路线竞争格局",
        "paper_dist_title": "论文技术路线分布",
        "paper_dist_x": "技术路线",
        "paper_dist_y": "论文数量",
        "trend_title": "技术路线热度趋势",
        "company_section": "公司技术路线分布",
        "company_pie_title": "公司技术路线占比",
        "no_topic_data": "暂无论文主题数据，请先运行主题模型",
        # 04_comparison
        "page_title_compare": "竞品对比 | EmbodiedIQ",
        "title_compare": "⚖️ 竞品对比",
        "select_company_a": "选择公司A",
        "select_company_b": "选择公司B",
        "chart_title_compare": "{c1} vs {c2} 多维度对比",
        "compare_metric": "指标",
        "compare_tech_route": "技术路线",
        "compare_funding_round": "最新融资轮次",
        "compare_funding_amount": "融资金额(百万元)",
        "compare_papers": "论文数(12月)",
        "compare_patents": "专利数(12月)",
        "compare_stars": "GitHub Stars",
        "compare_score": "综合评分",
        "select_diff_hint": "请选择两家不同的公司进行对比",
    }
}

SIGNAL_TYPE_MAP = {
    "en": {
        "Substantive_Growth": "Substantive Growth",
        "Funding_Driven": "Funding Driven",
        "Early_Signal": "Early Signal",
        "Low_Activity": "Low Activity",
    },
    "zh": {
        "Substantive_Growth": "实质进展型",
        "Funding_Driven": "融资驱动型",
        "Early_Signal": "早期信号型",
        "Low_Activity": "低活跃度",
    }
}

TECH_ROUTE_MAP = {
    "en": {
        "VLA_Models": "VLA Models",
        "Dexterous_Manipulation": "Dexterous Manipulation",
        "Humanoid_Control": "Humanoid Control",
        "Sim_to_Real": "Sim-to-Real",
        "Robot_Learning": "Robot Learning",
        "Grasping": "Grasping",
        "Navigation": "Navigation",
        "Multi_Modal": "Multi-Modal",
        "Other": "Other",
    },
    "zh": {
        "VLA_Models": "VLA模型",
        "Dexterous_Manipulation": "灵巧操作",
        "Humanoid_Control": "人形控制",
        "Sim_to_Real": "仿真到现实",
        "Robot_Learning": "机器人学习",
        "Grasping": "抓取",
        "Navigation": "导航",
        "Multi_Modal": "多模态",
        "Other": "其他",
    }
}


def init_language():
    if "language" not in st.session_state:
        st.session_state.language = "en"


def get_lang():
    init_language()
    return st.session_state.language


def t(key, lang=None):
    if lang is None:
        lang = get_lang()
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)


def translate_signal_type(val, lang=None):
    if lang is None:
        lang = get_lang()
    return SIGNAL_TYPE_MAP.get(lang, {}).get(val, val)


def translate_tech_route(val, lang=None):
    if lang is None:
        lang = get_lang()
    return TECH_ROUTE_MAP.get(lang, {}).get(val, val)


def render_language_selector():
    """在 sidebar 顶部渲染语言切换器。每个页面开头调用一次。"""
    init_language()
    current = st.session_state.language
    options = ["English", "中文"]
    index = 0 if current == "en" else 1
    selected = st.sidebar.radio(
        "🌐",
        options,
        index=index,
        horizontal=True,
        label_visibility="collapsed"
    )
    st.session_state.language = "en" if selected == "English" else "zh"
