import requests
import pandas as pd
import xml.etree.ElementTree as ET
import time
from datetime import datetime


def fetch_arxiv_for_month(year, month, max_results=60):
    """Fetch arXiv papers for a specific month using submittedDate range."""
    base_url = "http://export.arxiv.org/api/query"

    start_dt = datetime(year, month, 1)
    if month == 12:
        end_dt = datetime(year + 1, 1, 1)
    else:
        end_dt = datetime(year, month + 1, 1)

    start_str = start_dt.strftime("%Y%m%d%H%M%S")
    end_str = end_dt.strftime("%Y%m%d%H%M%S")

    search_query = (
        f"(cat:cs.RO OR cat:cs.AI OR cat:cs.CV) "
        f"AND (embodied intelligence OR humanoid robot OR robot learning) "
        f"AND submittedDate:[{start_str} TO {end_str}]"
    )

    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }

    resp = requests.get(base_url, params=params, timeout=60)
    if resp.status_code != 200:
        print(f"  Warning: status {resp.status_code} for {year}-{month:02d}")
        return pd.DataFrame()

    root = ET.fromstring(resp.content)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    entries = root.findall('atom:entry', ns)

    papers = []
    for entry in entries:
        cat_elem = entry.find('atom:category', ns)
        paper = {
            'title': entry.find('atom:title', ns).text.strip() if entry.find('atom:title', ns) is not None else '',
            'summary': entry.find('atom:summary', ns).text.strip() if entry.find('atom:summary', ns) is not None else '',
            'published': entry.find('atom:published', ns).text[:10] if entry.find('atom:published', ns) is not None else '',
            'authors': ', '.join([author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)]),
            'link': entry.find('atom:id', ns).text,
            'primary_category': cat_elem.get('term') if cat_elem is not None else ''
        }
        papers.append(paper)

    df = pd.DataFrame(papers)
    if not df.empty and 'published' in df.columns:
        df['published'] = pd.to_datetime(df['published'])
    print(f"  Fetched {len(df)} papers for {year}-{month:02d}")
    return df


def main():
    all_dfs = []
    months = [(2025, 10), (2025, 11), (2025, 12), (2026, 1), (2026, 2)]

    for year, month in months:
        print(f"Fetching {year}-{month:02d}...")
        df = fetch_arxiv_for_month(year, month, max_results=60)
        if not df.empty:
            all_dfs.append(df)
        time.sleep(3)  # Respect arXiv rate limit

    if all_dfs:
        new_papers = pd.concat(all_dfs, ignore_index=True)
        new_papers = new_papers.drop_duplicates(subset=['link'])
        output_path = '../data/raw/arxiv_papers_new_months.csv'
        new_papers.to_csv(output_path, index=False)
        print(f"\nSaved {len(new_papers)} new papers to {output_path}")
        print(new_papers.groupby(new_papers['published'].dt.to_period('M')).size())
    else:
        print("No new papers fetched.")


if __name__ == "__main__":
    main()
