import requests
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime

def fetch_arxiv_papers(query="embodied intelligence OR humanoid robot OR robot learning", 
                        max_results=100, 
                        date_from="20230101000000",
                        date_to="20260430235959"):
    """
    从arXiv获取具身智能相关论文
    query: 搜索关键词
    max_results: 最大返回数量（建议先100条测试）
    """
    base_url = "http://export.arxiv.org/api/query"
    
    # 构建查询（限定cs.RO机器人学、cs.AI人工智能、cs.CV计算机视觉）
    search_query = f"cat:cs.RO+OR+cat:cs.AI+OR+cat:cs.CV+AND+({query.replace(' ', '+')})"
    
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    
    response = requests.get(base_url, params=params, timeout=30)
    root = ET.fromstring(response.content)
    
    # arXiv API返回Atom格式
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
    
    df = pd.DataFrame(papers)
    if not df.empty and 'published' in df.columns:
        df['published'] = pd.to_datetime(df['published'])
        # 过滤时间范围
        date_from_str = date_from[:4]+'-'+date_from[4:6]+'-'+date_from[6:8]
        date_to_str = date_to[:4]+'-'+date_to[4:6]+'-'+date_to[6:8]
        df = df[(df['published'] >= date_from_str) & (df['published'] <= date_to_str)]
    
    print(f"成功获取 {len(df)} 篇论文")
    return df

if __name__ == "__main__":
    # 获取论文
    papers_df = fetch_arxiv_papers(max_results=100)
    print(papers_df.head())
    
    # 保存到CSV
    output_path = '../data/raw/arxiv_papers.csv'
    papers_df.to_csv(output_path, index=False)
    print(f"数据已保存到 {output_path}")
