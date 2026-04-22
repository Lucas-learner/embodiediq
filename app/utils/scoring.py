import pandas as pd
import numpy as np

def calculate_activity_score(company_row):
    """
    计算公司综合活跃度评分
    权重分配（可根据投资判断调整）：
    - 融资信号：30%
    - 学术信号：20%
    - 专利信号：20%
    - 开源信号：20%
    - 招聘信号：10%
    """
    funding_score = min(company_row.get('funding_count_12m', 0) * 20 + 
                       company_row.get('funding_amount_12m', 0) / 10, 100)
    
    paper_score = min(company_row.get('paper_count_12m', 0) * 15, 100)
    
    patent_score = min(company_row.get('patent_count_12m', 0) * 15, 100)
    
    opensource_score = min(company_row.get('github_stars', 0) / 50 + 
                          company_row.get('github_commits_12m', 0) / 10, 100)
    
    hiring_score = min(company_row.get('job_postings_12m', 0) * 10, 100)
    
    # 加权总分
    total = (funding_score * 0.3 + 
             paper_score * 0.2 + 
             patent_score * 0.2 + 
             opensource_score * 0.2 + 
             hiring_score * 0.1)
    
    return {
        'total_score': round(total, 1),
        'funding_score': round(funding_score, 1),
        'paper_score': round(paper_score, 1),
        'patent_score': round(patent_score, 1),
        'opensource_score': round(opensource_score, 1),
        'hiring_score': round(hiring_score, 1)
    }

def detect_signal_type(row):
    """
    热度去噪：判断是"融资驱动型"还是"实质进展型"
    """
    funding_high = row['funding_score'] > 60
    tech_high = (row['paper_score'] + row['patent_score']) > 80
    
    if funding_high and tech_high:
        return "Substantive_Growth"  # 实质进展型
    elif funding_high and not tech_high:
        return "Funding_Driven"      # 融资驱动型（可能是泡沫）
    elif not funding_high and tech_high:
        return "Early_Signal"        # 早期信号型（技术强但融资少=机会）
    else:
        return "Low_Activity"        # 低活跃度
