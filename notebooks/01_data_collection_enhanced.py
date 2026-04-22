"""
增强版论文数据采集 - 多关键词轮询 + 自动重试
目标：从arXiv获取150+篇具身智能相关论文
"""
import requests
import pandas as pd
import xml.etree.ElementTree as ET
import time
import os
from datetime import datetime

# 多组查询词，覆盖具身智能各技术方向
QUERIES = [
    "embodied intelligence",
    "humanoid robot",
    "robot learning",
    "dexterous manipulation",
    "visuomotor policy",
    "robotic grasping",
    "whole body control",
    "sim to real robot",
    "manipulation learning",
    "mobile manipulation",
]

def fetch_arxiv_papers(query, max_results=50, retries=3, delay=5):
    """获取arXiv论文，带重试机制"""
    base_url = "https://export.arxiv.org/api/query"
    search_query = f"cat:cs.RO+OR+cat:cs.AI+OR+cat:cs.CV+AND+({query.replace(' ', '+')})"
    
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    
    for attempt in range(retries):
        try:
            response = requests.get(base_url, params=params, timeout=30)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                papers = []
                for entry in root.findall('atom:entry', ns):
                    paper = {
                        'title': entry.find('atom:title', ns).text.strip() if entry.find('atom:title', ns) is not None else '',
                        'summary': entry.find('atom:summary', ns).text.strip() if entry.find('atom:summary', ns) is not None else '',
                        'published': entry.find('atom:published', ns).text[:10] if entry.find('atom:published', ns) is not None else '',
                        'authors': ', '.join([author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)]),
                        'link': entry.find('atom:id', ns).text,
                        'primary_category': entry.find('atom:category', ns).get('term') if entry.find('atom:category', ns) is not None else ''
                    }
                    papers.append(paper)
                return pd.DataFrame(papers)
            elif response.status_code in [429, 502, 503]:
                wait = delay * (attempt + 1)
                print(f"  [{query}] 状态码 {response.status_code}，等待 {wait}s 后重试...")
                time.sleep(wait)
            else:
                print(f"  [{query}] 错误状态码: {response.status_code}")
                return pd.DataFrame()
        except Exception as e:
            print(f"  [{query}] 请求异常: {e}")
            time.sleep(delay)
    
    return pd.DataFrame()

if __name__ == "__main__":
    all_papers = []
    existing_df = pd.DataFrame()
    
    # 尝试加载现有数据
    existing_path = '../data/raw/arxiv_papers.csv'
    if os.path.exists(existing_path):
        existing_df = pd.read_csv(existing_path)
        print(f"已加载现有数据: {len(existing_df)} 篇")
        all_papers.append(existing_df)
    
    # 轮询各关键词
    for i, query in enumerate(QUERIES):
        print(f"\n[{i+1}/{len(QUERIES)}] 查询: {query}")
        df = fetch_arxiv_papers(query, max_results=30)
        if not df.empty:
            print(f"  获取到 {len(df)} 篇")
            all_papers.append(df)
        else:
            print(f"  未获取到数据")
        time.sleep(3)  # 礼貌延迟
    
    # 合并去重
    if all_papers:
        combined = pd.concat(all_papers, ignore_index=True)
        if 'link' in combined.columns:
            combined = combined.drop_duplicates(subset=['link'])
        if 'published' in combined.columns:
            combined['published'] = pd.to_datetime(combined['published'])
            combined = combined[combined['published'] >= '2020-01-01']
        
        combined = combined.sort_values('published', ascending=False)
        print(f"\n✅ 合并后共 {len(combined)} 篇（去重后）")
        
        combined.to_csv(existing_path, index=False)
        print(f"数据已保存到 {existing_path}")
    else:
        print("\n⚠️ 未获取到任何数据")
