import pandas as pd
import os

def load_all_data():
    """加载所有数据源"""
    # 从utils目录向上两级到达项目根目录，再进入data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, '..', '..', 'data')
    
    result = {}
    
    # 加载公司数据（手工维护的核心列表）
    companies_path = os.path.join(data_dir, 'raw', 'funding_events.csv')
    if os.path.exists(companies_path):
        result['companies'] = pd.read_csv(companies_path)
    else:
        result['companies'] = pd.DataFrame()
    
    # 加载论文数据（API获取或种子数据）
    papers_path = os.path.join(data_dir, 'processed', 'papers_with_topics.csv')
    if os.path.exists(papers_path):
        result['papers'] = pd.read_csv(papers_path)
    else:
        # 降级：用原始数据
        raw_papers = os.path.join(data_dir, 'raw', 'arxiv_papers.csv')
        if os.path.exists(raw_papers):
            result['papers'] = pd.read_csv(raw_papers)
        else:
            result['papers'] = pd.DataFrame()
    
    # 加载融资数据
    if 'companies' in result and not result['companies'].empty:
        result['funding'] = result['companies'][['company_name', 'funding_date', 'funding_round', 'amount_rmb_m', 'investors']].dropna()
    else:
        result['funding'] = pd.DataFrame()
    
    # 加载GitHub开源数据
    github_path = os.path.join(data_dir, 'raw', 'github_repos.csv')
    if os.path.exists(github_path):
        result['github'] = pd.read_csv(github_path)
    else:
        result['github'] = pd.DataFrame()
    
    return result
